import requests
import functools
from http import HTTPStatus
from cache_loader import logger

BASE_URL = 'http://interview.agileengine.com'
AUTH_ROUTE = 'auth'
IMAGES_ROUTE = 'images'
API_KEY = '23567b218376f79d9415'


class TokenDecorator:
    _token = ''

    def __init__(self):
        self._fetch_token()

    def __call__(self, request_function):
        @functools.wraps(request_function)
        def wrap(*args):
            response = request_function(*args, token=self._token)
            if response.status_code == HTTPStatus.OK:
                return response
            elif response.status_code == HTTPStatus.UNAUTHORIZED:
                logger.info('Unauthorized. Refreshing token...')
                self._fetch_token()
                return request_function(*args)
        return wrap

    def _fetch_token(self):
        auth_response = requests.post(url=f'{BASE_URL}/{AUTH_ROUTE}/', json={'apiKey': API_KEY})
        if auth_response.status_code == HTTPStatus.OK:
            self._token = auth_response.json().get('token', '')
            logger.debug('Token received')
        else:
            logger.error('Error while fetching auth token!')


token_decorator = TokenDecorator()


@token_decorator
def get_images_by_page(page_num=1, token=''):
    return requests.get(f'{BASE_URL}/{IMAGES_ROUTE}?page={page_num}', headers=_prepare_headers(token))


@token_decorator
def get_image_details_by_id(image_id, token=''):
    return requests.get(f'{BASE_URL}/{IMAGES_ROUTE}/{image_id}', headers=_prepare_headers(token))


def _prepare_headers(token):
    return {'Authorization': f'Bearer {token}'}

