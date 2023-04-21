import time
import requests
import json
from pprint import pprint


class VkGetPhotos:

    def __init__(self, token: str):
        self.token = token

    def _get_params(self, owner_id, album_id, extended, 
        photo_sizes, count, api_version):

        params = {
        'owner_id': owner_id,
        'user_ids': owner_id,
        'album_id': album_id,
        'extended': extended,
        'photo_sizes': photo_sizes,
        'count': count,
        'access_token': self.token,
        'v': api_version,
        }
        return params
    
    def get_photos(self, owner_id, album_id='profile', extended=1, 
        photo_sizes=1, count=5, api_version='5.131'):

        URL = 'https://api.vk.com/method/photos.get'
        params = self._get_params(owner_id, album_id, extended, 
        photo_sizes, count, api_version)
        
        print(f'Отправляем запрос для получения информации о {count} фото пользователя Id={owner_id} в ВК')

        response = requests.get(URL, params)
        if response.status_code == 200:
            print(f'Информация о {count} фото пользователя Id={owner_id} успешно прочитана')
        else:
            print(f'Ошибка запроса {response.status_code}\nРабота программы остановлена')
            exit

        folder_name = self._get_user_name(params)
        file_name = f'{folder_name}.json' 

        with open(file_name, "w") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
            print(f'информация о {count} фото успешно сохранена в файл {file_name} в формате json')
        
        return response, folder_name

    def _get_user_name(self, params):
        URL = 'https://api.vk.com/method/users.get'
    
        response = requests.get(URL, params=params).json()

        for key in response['response']:
            first_name = key['first_name']
            last_name = key['last_name']
            id = key['id']
            print(f'Получена информация о пользователе VK с id={id}\nЭто {first_name} {last_name}')
        response = f'{id}_{first_name}_{last_name}'
        
        return response





            # for value in key:
        # pprint(response['response'])
        # print(type(response['response']))        
        # pprint(response.get('response').get('first_name'))
        # print(type(response.get('response')))

        # for key in response['response']:
        #     print(key)
        # pprint(response.json())
        # print(type(response.json()))
        # # pprint(response.json()['first_name'])
        # pprint(response.get('response').get('first_name'))
        # # pprint(response.json()['first_name'])

        return response


        # # pprint(response)
        # print(type(response))
        # print(response)
        # return response
        

    # def get_params(self, user_id, api_version='5.131', 
    #     extended=0, fields=''):

    #     params = {
    #     'user_ids': user_id,
    #     'access_token': token, # токен и версия api являются обязательными параметрами во всех запросах к vk
    #     'v': api_version,
    #     'extended':extended,
    #     'fields':fields
    #     }
    #     return params
    
    # def get_photo_list(user_id, )



        