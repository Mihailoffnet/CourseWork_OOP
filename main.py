# import requests
from pprint import pprint
from YaDiskUploader import YaUploader
from VK_get_photos import VkGetPhotos
from datetime import datetime
import time
import json



# загружаю токены из файла. 
# Первая строка - токен Яндекс диска,
# Вторая строка - токен ВК с правами scope = photos 

with open('token.txt', 'r') as file_object:
    yadisk_token = file_object.readline().strip()
    vk_token = file_object.readline().strip()

# тест класса VkGetPhotos

if __name__ == '__main__':

    # тест класса VkGetPhotos
    get_photo = VkGetPhotos(vk_token)

    # можно дополнительно указать параметры:
    # album_id='wall': фотографии со стены, 'saved' - сохраненные фотографии. 
    # по умолчанию загружаются фотографии профиля 'profile'
    # count=: количество загружаемых фотографий. По умолчанию 5
    # rev=: 1 - получить последние фото. 0 - получить более старые фото.
    # по умолчанию 1, получить более новые фото.
    # api_version= - версия api. По умолчанию '5.131'
    # значения по умолчанию можно изменить в функции get_photos
    # в классе VkGetPhotos
    result_photos = get_photo.get_photos(owner_id='5') # 2737213
    # print(result_photos[0].json())
    print()  
    pprint(result_photos[1])
    print()  
    pprint(result_photos[2])
    print()

    # тест класса YaUploader
    target_path = result_photos[2]
    filename = f'{target_path}.json'
    target_path_to_file = f'{target_path}/{filename}'
    path_to_file = filename

    uploader = YaUploader(yadisk_token)
    result_yadisk = uploader.upload(path_to_file, filename, target_path, target_path_to_file)
