import time

from environs import env

import requests

import telegram

import logging
from logging.handlers import RotatingFileHandler


def get_lesson_status(url, devman_token, timestamp=None):
    headers = {"Authorization": f"Token {devman_token}"}
    payload = {"timestamp": timestamp} if timestamp else None
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


class LogsHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)


def main():
    env.read_env()
    telegram_token = env("TELEGRAM_BOT_TOKEN")
    devman_token = env("DEVMAN_TOKEN")
    telegram_chat_id = "-1002385506480"
    url = "https://dvmn.org/api/long_polling/"
    bot = telegram.Bot(token=telegram_token)

    logger = logging.getLogger("telegram_bot")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler("app.log", maxBytes=200, backupCount=2)
    logger.addHandler(handler)

    logger.info("bot starting")

    timestamp = None

    while True:
        try:
            review_results = get_lesson_status(url, devman_token, timestamp)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            logging.error(
                "ConnectionError: No internet connection. Attempting to reconnect.."
            )
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
