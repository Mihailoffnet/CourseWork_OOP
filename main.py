
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
    # album_id='wall' - фотографии со стены, 'saved' - сохраненные фотографии. 
    # по умолчанию загружаются фотографии профиля
    # count= - количество загружаемых фотографий. По умолчанию 5
    # api_version= - версия api. По умолчанию '5.131'
    # значения по умолчанию можно изменить в функции get_photos
    # в классе VkGetPhotos
    result_photos = get_photo.get_photos(owner_id='1')
    # print(result_photos[0].json())
    print(result_photos[1])
    print(result_photos[2])
    print()


    # # создаем список словарей без лишних ключей
    # list_photos = result_photos[0].json().pop('response').pop('items')
    # # pprint(list_photos)
    # # print(type(list_photos))

    # # перебираем список словарей и составляем новый список
    # # содержащий только нужные данные по фото
    # list_photo = []
    # for dict in list_photos:
    #     temp_dict = {}
    #     temp_dict['id_photo'] = dict['id']
    #     temp_dict['likes_photo'] = dict['likes']['count']
    #     # дату фото для имени файла приводим в читаемый вид и формат str
    #     temp_dict['date_photo'] = str(datetime.fromtimestamp(dict['date']))[:-9]

    #     for types in dict['sizes']:
    #         if types['type'] == 's':
    #             size = types['type']
    #         elif types['type'] == 'm':
    #             size = types['type']
    #         elif types['type'] == 'x':
    #             size = types['type']     
    #         elif types['type'] == 'y':
    #             size = types['type']    
    #         elif types['type'] == 'z':
    #             size = types['type']       
    #         else: size = types['type']
    #     temp_dict['size'] = size 
    #     list_photo.append(temp_dict)
        
    # print(list_photo)
    # print()
    

        #         list.append()

            # for size in ['w', 'z', 'y', 'x', 'm', 's']:
            #     print(size)
            #     if types['type'] == size:
            #         print(f'самое большое изображение {size}')
            #         break
            # print(type(type))
            # print()


    # # тест класса YaUploader
    # target_path = result_photos[1]
    # filename = f'{target_path}.json'
    # target_path_to_file = f'{target_path}/{filename}'
    # path_to_file = filename

    # uploader = YaUploader(yadisk_token)
    # result_yadisk = uploader.upload(path_to_file, filename, target_path, target_path_to_file)