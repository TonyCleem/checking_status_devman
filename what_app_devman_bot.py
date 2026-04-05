import time

from environs import env

import requests

import telegram


def get_lesson_status(url, devman_token, timestamp=None):
    headers = {"Authorization": f"Token {devman_token}"}
    payload = {"timestamp": timestamp} if timestamp else None
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


def main():
    env.read_env()
    telegram_token = env("TELEGRAM_BOT_TOKEN")
    devman_token = env("DEVMAN_TOKEN")
    telegram_chat_id = input("Введите чат ID:")
    url = "https://dvmn.org/api/long_polling/"
    bot = telegram.Bot(token=telegram_token)

    timestamp = None
    while True:
        try:
            review_results = get_lesson_status(url, devman_token, timestamp)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            print("ConnectionError: No internet connection\nAttempt to reconnect")
            time.sleep(30)
            continue

        if review_results["status"] == "timeout":
            timestamp = review_results["timestamp_to_request"]
            continue

        if review_results["status"] == "found":
            works = review_results["new_attempts"]
            for work in works:
                review_message = (
                    f'У Вас проверили работу "{work["lesson_title"]}\n'
                    f"Ссылка на работу {work['lesson_url']}\n\n"
                )
                if work["is_negative"]:
                    bot.send_message(
                        telegram_chat_id,
                        review_message + "К сожалению в работе нашлись ошибки.",
                    )
                else:
                    bot.send_message(
                        telegram_chat_id,
                        review_message
                        + "Преподователю все понравилось, можно приступать к следующему уроку!",
                    )


if __name__ == "__main__":
    main()
