from YaDiskUploader import YaUploader
from VK_get_photos import VkGetPhotos
import logging


logging.basicConfig(level=logging.DEBUG, filename="py_log.log",filemode="a", format='%(asctime)s %(levelname)s %(message)s')
# logging.debug("A DEBUG Message")
# logging.info("An INFO")
# logging.warning("A WARNING")
# logging.error("An ERROR")
# logging.critical("A message of CRITICAL severity")



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
    result_photos = get_photo.get_photos(owner_id='pisatelnaminimalkah', count=5) 
    # 2737213 51030512 245760700
    # print(result_photos[0].json())
    # print()  
    # pprint(result_photos[1])
    # print()  
    # pprint(result_photos[2])
    # print()

    # тест класса YaUploader

    uploader = YaUploader(yadisk_token)
    result_yadisk1 = uploader.list_upload(result_photos[1], result_photos[2])
