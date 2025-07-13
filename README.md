# checking_status_devman

checking_status_devman - бот для проверки статуса отправленной на проверку работы.


## Фунцкионал
**what_app_devman_bot.py** - основной скрипт для запуска. После запуска проверяет статус используя Long Polling соединение.

## Установка

#### Подготовка окружения

Python3 должен быть уже установлен.

#### Клонируйте репозиторий:
```commandline
git clone https://github.com/TonyCleem/checking_status_devman
```
#### Установите и активируйте _*venv*_ в зависимости от вашей OS:
Для получения информации ознакомьтесь с [документацией](https://docs.python.org/3/tutorial/venv.html).

#### **"requirements.txt"**

После активации виртуального окружения установите все зависимости командой:
```
pip install -r requirements.txt
```

#### API

Для работы требуются токены API, а также id чата Телеграм:
- Токен Devman
- [Telegram](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/#02:~:text=%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B%2C%20%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D0%B8%C2%BB.-,%D0%A1%D0%BE%D0%B7%D0%B4%D0%B0%D0%B5%D0%BC%20%D0%B1%D0%BE%D1%82%D0%B0,-%D0%A1%D0%BB%D0%B5%D0%B4%D1%83%D1%8E%D1%89%D0%B8%D0%B9%20%D1%88%D0%B0%D0%B3%20%E2%80%94%20%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5)
- [@userinfobot](https://telegram.me/userinfobot)

Полученные токены укажите в переменных файла `.env`.

Пример файла `.env`:
>```
>DEVMAN_TOKEN=<ваш ключ>
>TELEGRAM_BOT_TOKEN=<токен от вашего бота>
>```

#### Telegram bot

Создаем бота через [BotFather](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html)


## Использование ##

- Перейти в склонированный репозиторий и запустить скрипт:
```commandline
python3 what_app_devman_bot.py
```
- После чего необходимо указать ID чата.

```shell
Введите чат ID: <id>
```
ID чата можно запросить у бота [@userinfobot](https://github.com/nadam/userinfobot)