from YaDiskUploader import YaUploader
from VK_get_photos import VkGetPhotos

# текстовые переменные
welcome = '''Программа для загрузки фото из VK в Яндекс диск.
Для работы программы вам понадобится токен ЯндексДиска.

В простом режиме программа загружает 5 файлов из профиля (с аватара) пользователя по заданному id или логину пользователя. 

В расширенном режиме можно загружать неограниченное количество фотографий из профиля, со стены пользователя или из его альбома.'''
mode = '''
Хотите запустить программу в расширенном режиме? Ответьте "2".
Чтобы продолжить в упрощенном режиме, ответьте "1" или нажмите Enter.
Ваш выбор: '''
token_text = '''
Скопируйте сюда свой OAuth-токен яндекс диска.
OAuth-токен можно получить по адресу: https://yandex.ru/dev/disk/rest/
Или нажмите Enter, если хотите использовать ранее введенный токен.
Ваш OAuth-токен: '''
take_id = 'Введите id или login пользователя VK: '
take_album = '''
Скачать фото со стены - ответьте "2"
Скачать фото из профиля - ответьте "1" или нажмите Enter.
Ваш выбор: '''
count_photo = '''
Введите количество фотографий, которые нужно скачать. 
Если у пользователя окажется меньше фотографий, то будут скачаны все.
Ваш выбор: '''

# загружаю токен ВК из файла
with open('token_vk.txt', 'r') as file_object:
    vk_token = file_object.readline().strip()

# функция для объединения функционала двух классов


def safe_photo(owner_id, album_id='profile', extended=1,
               photo_sizes=1, count=5, rev=1, api_version='5.131'):
    get_photo = VkGetPhotos(vk_token)
    uploader = YaUploader(yadisk_token)
    result_photos = get_photo.get_photos(owner_id, album_id, extended,
                                         photo_sizes, count, rev, api_version)
    result_yadisk = uploader.list_upload(result_photos[1], result_photos[2])


# запускаем программу
if __name__ == '__main__':
    print(welcome)
    chose = input(mode)
    yadisk_token = ''
    while len(yadisk_token) <= 0:
        yadisk_token = input(token_text)
        if yadisk_token == '':
            with open('token_yd.txt', 'r') as file_object:
                yadisk_token = file_object.readline().strip()
    uploader = YaUploader(yadisk_token)
    uploader.test_token()
    with open('token_yd.txt', 'w') as file:
        file.write(yadisk_token.strip())
    id = ''
    while id == '':
        print()
        id = input(take_id).lower()
        print()
    if chose != '2':
        safe_photo(owner_id=id)
    else:
        x = input(take_album)
        if x == '2':
            a_id = 'wall'
        else:
            a_id = 'profile'
        y = ''
        while not y.isnumeric():
            y = input(count_photo)
            print()
        count_photo = int(y)
        safe_photo(owner_id=id, album_id=a_id, count=count_photo)
