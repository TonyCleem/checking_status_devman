import requests
import json
import pprint
from environs import env
from dotenv import load_dotenv


def get_lesso_status(url, devman_token):
    headers = {
        'Authorization': f'Token {devman_token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()   
    pprint.pprint(response.json())


if __name__ == "__main__":
    load_dotenv()
    devman_token = env.str('TOKEN_DEVMAN')
    url = 'https://dvmn.org/api/long_polling/'
    get_lesso_status(url, devman_token)