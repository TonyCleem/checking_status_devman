import sys
import time

from environs import env

import requests

import telegram


def error_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_lesson_status(url, devman_token):
    headers = {
        'Authorization': f'Token {devman_token}'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        status = response.json()
        return status
    except requests.exceptions.ReadTimeout as error:
        error_print(error)
    except requests.exceptions.ConnectionError as error:
        print('ConnectionError: No internet connection\nAttempt to reconnect')
        time.sleep(10)
        error_print(error)


def get_new_lesson_status(url, devman_token, timestamp):
    headers = {
        'Authorization': f'Token {devman_token}'
    }
    payload = {
        'timestamp': f'{timestamp}'
    }
    try:
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        status = response.json()
        return status
    except requests.exceptions.ReadTimeout as error:
        error_print(error)
    except requests.exceptions.ConnectionError as error:
        print('ConnectionError: No internet connection\nAttempt to reconnect')
        time.sleep(10)
        error_print(error)


if __name__ == "__main__":
    env.read_env()
    telegram_token = env('TELEGRAM_BOT_TOKEN')
    devman_token = env('DEVMAN_TOKEN')
    telegram_chat_id = input('Введите чат ID: ')
    url = 'https://dvmn.org/api/long_polling/'
    bot = telegram.Bot(token=telegram_token)
    review_results = get_lesson_status(url, devman_token)

    while True:
        if review_results['status'] == 'timeout':
            timestamp = review_results['timestamp_to_request']
            review_results = get_new_lesson_status(url, devman_token, timestamp)
        if review_results['status'] == 'found':
            print(review_results)
            works = review_results['new_attempts']
            for work in works:
                timestamp = work['timestamp']
                review_message = (
                        f'У Вас проверили работу "{work['lesson_title']}\n'
                        f'Ссылка на работу {work['lesson_url']}\n\n'
                )
                if work['is_negative']:
                    bot.send_message(
                        telegram_chat_id, review_message + "К сожалению в работе нашлись ошибки."
                    )

                if not work['is_negative']:
                    bot.send_message(
                        telegram_chat_id, review_message + "Преподователю все понравилось, можно приступать к следующему уроку!"
                    )
        break
