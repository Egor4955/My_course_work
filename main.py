import requests
import json
from tqdm import tqdm

access_token = '...' # Нужно вставить VK токен
user_id = input('Введите VK id: ')


class VkDownloader:
    def __init__(self):
        self.token = access_token

    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': user_id,
            'access_token': access_token,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes':1, 
            'v':'5.131'
            }
        res = requests.get(url=url, params=params)
        return res.json()
    
    def get_all_photos(self):
        photo_max_size_url = {}
        data = self.get_photos()
        for photo in data['response']['items']:
            likes = photo['likes']['count']
            if likes not in photo_max_size_url.keys():
                likes = likes 
            else:
                likes = f"{likes}_{photo['date']}"
            sorted_list = list(sorted(photo['sizes'], key=lambda x: x['height'], reverse=True))
            photo_max_size_url[likes] = {'size':sorted_list[0]['type'], 'url':sorted_list[0]['url']}
        return photo_max_size_url


class Yandex:
    def __init__(self, token):
        self.token = token

    def folder_creation(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = {'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'}
        params = {'path': f'{folder_name}'}
        requests.put(url=url, headers=headers, params=params)

    def upload(self, photos):
        self.folder_creation()
        json_list = []
        for key, value in tqdm(photos.items()):
            yandex_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            url = value['url']
            size = value['size']
            headers = {
            'Content-Type': 'application/json',
            'Authorization': f"OAuth {self.token}"
            }
            params = {
            'url': url,
            'path': f"{folder_name}/{key}",
            'overwrite': 'false'
                }
            requests.post(url = yandex_url ,headers=headers, params=params)
            dict_for_json = {}
            dict_for_json['file_name']= key
            dict_for_json['size']= size
            json_list.append(dict_for_json)
        with open('photos.json', 'w') as file:
            json.dump(json_list, file)


downloader = VkDownloader()
photos = downloader.get_all_photos()
token_ya = f"{input('Введите Яндекс токен: ')}"
ya_downloader = Yandex(token_ya)
folder_name = input('Введите имя папки: ')
ya_downloader.upload(photos)