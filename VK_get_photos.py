import requests
import json
from datetime import datetime
from pprint import pprint
from Logger import Logger
import logging
import os


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

        Logger.get_logging(f'Отправляем запрос для получения информации о {count} фото пользователя Id={owner_id} в VK')

        # запрашиваем имя пользователя и создаем имя папки для загрузки
        folder_name = self._get_user_name(params)
        file_name = f'{folder_name}.json'
        
        # запрашгиваем информацию о фото  
        response = requests.get(URL, params, timeout=10)
        # count_photo = len(self._get_list_photo(response))
        if 'error' in response.json():
            error_code = response.json()['error']['error_code']
            error_msg = response.json()['error']['error_msg']
            Logger.get_logging(f'Ошибка: {error_msg}. Код ошибки: {error_code}. Работа программы остановлена.')
            exit(0)
        print
        if response.status_code == 200:
            Logger.get_logging(f'Информация о фото пользователя Id={owner_id} успешно прочитана.')
        else:
            Logger.get_logging(f'Ошибка запроса {response.status_code}. Работа программы остановлена.')    
            exit(0)

#         with open(file_name, "w") as f:
#             json.dump(response.json(), f, ensure_ascii=False, indent=4)
#         Logger.get_logging(f'Информация о последних фото успешно сохранена в файл {file_name} в формате json.') 
        Logger.get_logging(f'Выбрали самые большие фотографии загруженных фото пользователя Id={owner_id}.')    
        list_photos = self._get_list_photo(response)
           
        return response, list_photos, folder_name

    def _get_user_name(self, params):
        URL = 'https://api.vk.com/method/users.get'
    
        response = requests.get(URL, params=params, timeout=10).json()
        for key in response['response']:
            first_name = key['first_name']
            last_name = key['last_name']
            id = key['id']
            Logger.get_logging(f'Получена информация о пользователе VK с id={id}. Это {first_name} {last_name}.') 

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

        file_list = []
        for line in list_photo:
            temp_dict = {}
            temp_dict['size'] = line['size']
            name = line['likes_photo']
            if f'{name}.jpg' in temp_dict.keys():
                date_photo = line['date_photo']
                temp_dict['file_name'] = f'{name}_{date_photo}.jpg'
            else:
                temp_dict['file_name'] = f'{name}.jpg'
            file_list.append(temp_dict)
            url = line['url']
            target_file_name = temp_dict['file_name']
            response = requests.get(url)
            size = temp_dict['size']
            with open(target_file_name, 'wb') as file:
                file.write(response.content)
            Logger.get_logging(f'Файл {target_file_name} размера {size} сохранен на диск.')
        
        return file_list





        
