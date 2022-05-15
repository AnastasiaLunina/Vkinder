from time import sleep
import requests
import config
import webbrowser
from random import randint
from models import Session, engine
import models
import logger


class VkApi:
    """
    Creates a class to work with API vkontakte
    """

    def __init__(self):
        self.token = self._check_valid_token()
        # self.token = config.token_vkinder
        self.params = {
            'access_token': self.token,
            'v': '5.131'
        }
        self.offset = randint(0, 50)
        self.wish_list = []
        self.black_list = []

    @staticmethod
    def _access_code():
        """
        Initialize the object's state.
        Access_token and Version must be present in parameters
        """
        endpoint = 'https://oauth.vk.com/authorize'
        params = {
            'client_id': config.app_id,
            'display': 'page',
            'redirect_uri': config.redirect_uri,
            'scope': config.scope,
            'response_type': 'code',
            'v': '5.131'
        }
        try:
            response = requests.get(url=endpoint, params=params)
            if response.status_code != 200:
                raise ConnectionError
        except ConnectionError:
            logger.error_func(response.json())
            print('Ошибка при получении кода')
        else:
            webbrowser.open(response.url)
            code = input('Введите код с браузера: ').split('code=')[1]
            return code

    def _access_token(self):
        endpoint = 'https://oauth.vk.com/access_token'
        params = {
            'client_id': config.app_id,
            'client_secret': config.client_secret,
            'redirect_uri': config.redirect_uri,
            'code': self._access_code()
        }
        try:
            response = requests.get(url=endpoint, params=params)
            if response.status_code != 200:
                raise ConnectionError
        except ConnectionError:
            logger.error_func(response.json())
            print('Ошибка при получении токена')
        else:
            with open('token.txt', 'w', encoding='utf-8') as file:
                file.write(response.json()['access_token'])
            return response.json()['access_token']

    def _check_valid_token(self):
        with open('token.txt', 'r', encoding='utf-8') as file:
            accses_token = file.read().strip()
        endpoint = f'{config.base_url}secure.checkToken'
        params = {
            'access_token': config.service_key,
            'token': accses_token,
            'v': '5.131'
        }
        responce = requests.get(url=endpoint, params=params)
        if accses_token and responce.json().get('response').get('success') == 1:
            return accses_token
        else:
            return self._access_token()

    def search_user(self, city, sex, birth_year, count=1):
        """
        Sends API get request with requests package, using vk API method users.search with following parameters:
        'count', 'sex', 'birth_year', 'has_photo', 'has_photo',
        'hometown', 'offset' to get the information about match.
        If user profile is private, user is skipped to the next one.
        If user is in black list, user is skipped to the next one.
        Returns information about user in following format:
        First name, Last name
        Profile link
        three photos as attachments, taken from method get_photos_from_profile()
        """
        endpoint = f'{config.base_url}users.search'
        while True:
            self.offset += count
            params = {
                'count': count,
                'sex': sex,
                'birth_year': birth_year,
                'has_photo': 1,
                'hometown': city,
                'offset': self.offset
            }
            try:
                response = requests.get(url=endpoint, params={**params, **self.params})
                if not response.json()['response']['items']:
                    continue
                if response.status_code != 200:
                    raise ConnectionError
            except ConnectionError:
                logger.error_func(response.json())
                sleep(0.33)
                continue
            else:
                person = response.json()['response']['items'][0]
                if person['is_closed'] is True:
                    sleep(0.33)
                    continue
            session = Session()
            connection = engine.connect()
            if session.query(models.BlackList.vk_user_id).filter_by(vk_user_id=person["id"]).first() is not None:
                continue
            photo_profile = self.get_photos_from_profile(person['id'])
            return person['first_name'], person['last_name'], f'{config.base_profile_url}{person["id"]}', photo_profile

    def get_user_info(self, user_id):
        """
        Sends API get request with requests package, using vk API method users.get with following parameters:
        'user_ids', 'fields': 'bdate, sex, home_town', 'city' to get the information about bot user.
        If city information is missing, Moscow is used by default.
        If bdate information is missing, it generates randomly using randint.
        If sex information is missing, it generates randomly using randint.
        Returns city, sex, bdate of bot user.
        """
        endpoint = f'{config.base_url}users.get'
        params = {
            'user_ids': user_id,
            'fields': 'bdate, sex, home_town, city'
        }
        try:
            response = requests.get(url=endpoint, params={**params, **self.params})
            if response.status_code != 200:
                raise ConnectionError
        except ConnectionError:
            logger.error_func(response.json())
        else:
            data = response.json()['response'][0]
            if data.get('city', None) is None:
                city = 'Москва'
            else:
                city = data.get('city').get('title')
            if data.get('bdate', None) is None or len(data.get('bdate').split('.')) < 3:
                bdate = randint(1990, 2000)
            else:
                bdate = int(data.get('bdate').split('.')[2])
            if data.get('sex', None) is None:
                sex = randint(0, 2)
            else:
                if data.get('sex') == 2:
                    sex = 1
                else:
                    sex = 2
            return city, sex, bdate

    def get_photos_from_profile(self, user_id):
        """
        Sends API get request with requests package, using vk API method photos.get with following parameters:
        'owner_id', 'album_id', 'extended' to return additional fields (likes).
        Method chooses the three user's photo with the most amount of likes.
        Returns
        """
        sleep(0.33)
        result = []
        endpoint = f'{config.base_url}photos.get'
        params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
        }
        try:
            response = requests.get(endpoint, params={**self.params, **self.params, **params})
            response.raise_for_status()
            if response.status_code != 200:
                raise ConnectionError
            for foto in sorted(response.json()['response']['items'], key=lambda x: x['likes']['count'], reverse=True):
                result.append(f"photo{foto['owner_id']}_{foto['id']}")
                if len(result) == 3:
                    break
            return ','.join(result)
        except ConnectionError:
            logger.error_func(response.json())

