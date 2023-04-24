import time
import requests
import json
from datetime import datetime
from pprint import pprint


class VkGetPhotos:

    def __init__(self, token: str):
        self.token = token

    def _get_params(self, owner_id, album_id, extended, 
        photo_sizes, count, rev, api_version):

        params = {
        'owner_id': owner_id,
        'user_ids': owner_id,
        'rev': rev,
        'album_id': album_id,
        'extended': extended,
        'photo_sizes': photo_sizes,
        'count': count,
        'access_token': self.token,
        'v': api_version,
        }
        return params
    
    def get_photos(self, owner_id, album_id='profile', extended=1, 
        photo_sizes=1, count=5, rev=1, api_version='5.131'):

        URL = 'https://api.vk.com/method/photos.get'
        params = self._get_params(owner_id, album_id, extended, 
        photo_sizes, count, rev, api_version)

        log_line = f'{str(datetime.now())[:-4]}: Отправляем запрос для получения информации о {count} фото пользователя Id={owner_id} в VK'
        with open('logs.txt', 'w') as file:
            file.write(f'{log_line}\n')
        print(log_line)
        
        response = requests.get(URL, params)
        if 'error' in response.json():
            error_code = response.json()['error']['error_code']
            error_msg = response.json()['error']['error_msg']
            log_line = f'{str(datetime.now())[:-4]}: Ошибка: {error_msg}. Код ошибки: {error_code}. Работа программы остановлена.'
            with open('logs.txt', 'a') as file:
                file.write(f'{log_line}\n')
            print(log_line)
            exit(0)
            # if response.json()['error']['error_code'] == 30:
            #     log_line = f'{str(datetime.now())[:-4]}: Приватный профиль. Загрузка фото невозможна. Работа программы остановлена'
            #     with open('logs.txt', 'a') as file:
            #         file.write(f'{log_line}\n')
            #     print(log_line)
            #     exit(0)
            # elif response.json()['error']['error_code'] == 15:
            #     log_line = f'{str(datetime.now())[:-4]}: Доступ запрещен, аккаунт пользовтаеля был удален. Загрузка фото невозможна. Работа программы остановлена'
            #     with open('logs.txt', 'a') as file:
            #         file.write(f'{log_line}\n')
            #     print(log_line)
            #     exit(0)
            # else:
                # log_line = f'{str(datetime.now())[:-4]}: Ошибка {response.json()['error']['error_msg']} код ошибки {response.json()['error']['error_code']}. Работа программы остановлена'
                # with open('logs.txt', 'a') as file:
                #     file.write(f'{log_line}\n')
                # print(log_line)
                # exit(0)


        if response.status_code == 200:
            log_line = f'{str(datetime.now())[:-4]}: Информация о {count} фото пользователя Id={owner_id} успешно прочитана'
            with open('logs.txt', 'a') as file:
                file.write(f'{log_line}\n')
            print(log_line)
        else:
            log_line = f'{str(datetime.now())[:-4]}: Ошибка запроса {response.status_code}. Работа программы остановлена'
            with open('logs.txt', 'a') as file:
                file.write(f'{log_line}\n')
            print(log_line)
            exit(0)

        # получаем имя пользователя и создаем имя папки для загрузки
        folder_name = self._get_user_name(params)
        file_name = f'{folder_name}.json' 

        with open(file_name, "w") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        log_line = f'{str(datetime.now())[:-4]}: Информация о {count} последних фото успешно сохранена в файл {file_name} в формате json'
        with open('logs.txt', 'a') as file:
            file.write(f'{log_line}\n')          
        print(log_line)

        list_photos = self._get_list_photo(response)
        log_line = f'{str(datetime.now())[:-4]}: Выбрали самые большие фотографии из {count} загруженных фото пользователя Id={owner_id}'
        with open('logs.txt', 'a') as file:
            file.write(f'{log_line}\n')
        print(log_line)
            
        return response, list_photos, folder_name

    def _get_user_name(self, params):
        URL = 'https://api.vk.com/method/users.get'
    
        response = requests.get(URL, params=params).json()
        for key in response['response']:
            first_name = key['first_name']
            last_name = key['last_name']
            id = key['id']
            log_line = f'{str(datetime.now())[:-4]}: Получена информация о пользователе VK с id={id}. Это {first_name} {last_name}'
            with open('logs.txt', 'a') as file:
                file.write(f'{log_line}\n')
            print(log_line)
        response = f'{id}_{first_name}_{last_name}'
        
        return response

    def _get_list_photo(self, response):
        # создаем список словарей без лишних ключей
        list_photos = response.json().pop('response').pop('items')

        # перебираем список словарей и составляем новый список
        # содержащий только нужные данные по фото
        list_photo = []
        for dict in list_photos:
            temp_dict = {}
            temp_dict['id_photo'] = dict['id']
            temp_dict['likes_photo'] = dict['likes']['count']
            # дату фото для имени файла приводим в читаемый вид и формат str
            temp_dict['date_photo'] = str(datetime.fromtimestamp(dict['date']))[:-9]
            
            # print(len(dict['sizes']))
            # print(dict['sizes'])
            for types in dict['sizes']:
                if types['type'] == 's':
                    size = types['type']
                    url = types['url']
                elif types['type'] == 'm':
                    size = types['type']
                    url = types['url']
                elif types['type'] == 'x':
                    size = types['type']  
                    url = types['url']   
                elif types['type'] == 'y':
                    size = types['type']    
                    url = types['url']
                elif types['type'] == 'z':
                    size = types['type']    
                    url = types['url']   
                else: 
                    size = types['type']
                    url = types['url']
            temp_dict['size'] = size 
            temp_dict['url'] = url 
            list_photo.append(temp_dict)
        
        return list_photo




        
