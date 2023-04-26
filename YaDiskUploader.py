import requests
# from datetime import datetime
import json
from pprint import pprint
from Logger import Logger
import os


class YaUploader:

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def test_token(self):
        url = 'https://cloud-api.yandex.net/v1/disk'
        headers = self.get_headers()
        response = requests.get(url = url, headers=headers, timeout=5)
        code = response.status_code
        if code != 200:
            message = response.json()['message']
            Logger.get_logging(f'Ошибка токена: {code} - {message}. Проверьте правильность введенного OAuth-токена Яндекс диска. Работа программы остановлена\n')
            exit(0)
        else:
            Logger.get_logging(f'Токен яндекс диска проверен. Доступ предоставлен.')
  
    def _upload_link(self, target_path_to_file, target_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": target_path_to_file, "overwrite": "True"}
        response = requests.get(upload_url, headers=headers, 
                                params=params, timeout=10)
        if response.status_code == 409:
            Logger.get_logging(f'Пути {target_path} На Ядиске не существует.')
            self._great_folder(target_path)
            response = requests.get(upload_url, headers=headers, 
                                    params=params, timeout=10)
            Logger.get_logging(f'Папка {target_path} создана. Начинаем загрузку файла.')
        return response.json()

    def upload(self, path_to_file, filename, target_path, target_path_to_file):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        Logger.get_logging(f'Запрашиваем ссылку для загрузки файла.')
        href = self._upload_link(target_path_to_file, target_path)
        url = href.get('href')
        Logger.get_logging(f'Получена ссылка для загрузки файла.')
        response = requests.put(url, data=open(path_to_file, 'rb'), timeout=120)
        response.raise_for_status()
        if response.status_code == 201:
            Logger.get_logging(f'Файл {filename} успешно загружен на Яндекс Диск в папку {target_path}.')
        else:
            Logger.get_logging(f'Ошибка загрузки файла {response.status_code}. Работа программы остановлена.')
            exit(0)

    # функция для создания папки в яндекс диске
    def _great_folder(self, target_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': target_path}
        response = requests.put(url=url, headers=headers, params=params,
                                timeout=10)
        return response   
      
    # функция загрузки файлов из списка
    def list_upload(self, list, target_path):
        for photo in list:
            path_to_file = photo['file_name']
            target_file_name = path_to_file
            target_path_to_file = f'{target_path}/{path_to_file}'
            self.upload(path_to_file, target_file_name, target_path, target_path_to_file)
            os.remove(path_to_file)
            Logger.get_logging(f'Временный файл {path_to_file} удален.')
        dict_json = {}
        dict_json['files'] = list
        file_name = f'{target_path}.json'
        with open(file_name, 'w') as file:
            json.dump(dict_json, file, ensure_ascii=False, indent=4)
        Logger.get_logging(f'Файл {file_name} успешно сохранен.')
        Logger.get_logging(f'Работа программы завершена. Загружено {len(list)} файлов.\n')  
