
# import requests
from pprint import pprint
from YaDiskUploader import YaUploader
from VK_get_photos import VkGetPhotos

# загружаю токеный из файла. 
# Первая строка - токен Яндекс диска,
# Вторая строка - токен ВК с правами photos 

with open('token.txt', 'r') as file_object:
    yadisk_token = file_object.readline().strip()
    vk_token = file_object.readline().strip()
# print(yadisk_token)
# print(vk_token)
# print()

# тест класса VkGetPhotos

if __name__ == '__main__':

    # тест класса VkGetPhotos
    get_photo = VkGetPhotos(vk_token)
    result_photos = get_photo.get_photos(owner_id='2737213', album_id='wall')
    # pprint(result_photos[0].json())
    # print(result_photos[1])

    # тест класса YaUploader
    target_path = result_photos[1]
    filename = f'{target_path}.json'
    target_path_to_file = f'{target_path}/{filename}'
    path_to_file = filename

    uploader = YaUploader(yadisk_token)
    result_yadisk = uploader.upload(path_to_file, filename, target_path, target_path_to_file)