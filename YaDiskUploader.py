import requests
from datetime import datetime
from pprint import pprint

class YaUploader:

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _upload_link(self, target_path_to_file, target_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": target_path_to_file, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        # print(response.status_code)
        if response.status_code == 409:
            # print(response.status_code)
            log_line = f'{str(datetime.now())[:-4]}: Пути {target_path} На Ядиске не существует'
            with open('logs.txt', 'a') as file:
                file.write(f'{log_line}\n')
            print(log_line)
            self._great_folder(target_path)
            response = requests.get(upload_url, headers=headers, params=params)
            log_line = f'{str(datetime.now())[:-4]}: Папка {target_path} создана. Начинаем загрузку файла'
            with open('logs.txt', 'a') as file:
                file.write(f'{log_line}\n')
            print(log_line)
        return response.json()

    def upload(self, path_to_file, filename, target_path, target_path_to_file):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        log_line = f'{str(datetime.now())[:-4]}: Запрашиваем ссылку для загрузки файла'
        with open('logs.txt', 'a') as file:
            file.write(f'{log_line}\n')
        print(log_line)        
        href = self._upload_link(target_path_to_file, target_path)
        url = href.get('href')
        log_line = f'{str(datetime.now())[:-4]}: Получена ссылка для загрузки файла'
        with open('logs.txt', 'a') as file:
            file.write(f'{log_line}\n')
        response = requests.put(url, data=open(path_to_file, 'rb'))
        response.raise_for_status()
        # print(response.status_code)
        if response.status_code == 201:
            log_line = f'{str(datetime.now())[:-4]}: Файл {filename} успешно загружен на Яндекс Диск в папку {target_path}'
            with open('logs.txt', 'a') as file:
                file.write(f'{log_line}\n')
            print(log_line)    
        else:
            log_line = f'{str(datetime.now())[:-4]}: Ошибка загрузки файла {response.status_code}. Работа программы остановлена'
            with open('logs.txt', 'a') as file:
                file.write(f'{log_line}\n')
            print(log_line)   

    # функция для создания папки в яндекс диске, если указанного пути не существует

    def _great_folder(self, target_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {"path": target_path}
        response = requests.put(url=url, headers=headers, params=params)
        # print(response.status_code)
        return response    



