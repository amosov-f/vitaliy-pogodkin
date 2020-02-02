import json
import logging
from datetime import datetime

import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


def start(bot, update):
    update.message.reply_text('Всем добра и быть добрее!')


def pass_location(bot, update):
    print(update.message.location)
    location = update.message.location
    lon = location.longitude
    lat = location.latitude

    result = get_weather(lat, lon)

    answer = ''
    for date, temp, condition in result:
        day = datetime.strptime(date, '%Y-%m-%d')
        order = day.weekday()
        week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        week_day = week[order]

        sign = '+' if temp > 0 else ''

        icons = {
            'cloudy': '☁',
            'clear': '🌞',
            'partly-cloudy': '⛅',
            'overcast-and-light-rain': '🌦',
            'overcast': '🌪',
            'cloudy-and-light-rain': '🌧'
        }
        icon = icons[condition] if condition in icons else f'не шмог {condition}'

        answer += f'{week_day}: {sign}{temp}°C {icon}\n'

    update.message.reply_text(answer)


def get_weather(lat, lon):
    url = f'https://api.weather.yandex.ru/v1/forecast?lat={lat}&lon={lon}'
    print(url)
    response = requests.get(url, headers={
        'X-Yandex-API-Key': 'e6dcb2f6-e5c4-4a6d-b857-13d259a64dbd'
    })
    response.raise_for_status()
    response_json = response.json()

    result = []
    for forecast in response_json['forecasts']:
        date = forecast['date']
        day_short = forecast['parts']['day_short']
        temp = day_short['temp']
        condition = day_short['condition']
        result.append((date, temp, condition))

    return result

def code(bot, update):
    update.message.reply_text('https://github.com/amosov-f/vitaliy-pogodkin')


def start_bot():
    updater = Updater("930754446:AAHMBGcbo07gitLHIYZ_JeReysaavX7RwAY")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("code", code))
    dp.add_handler(MessageHandler(Filters.location, pass_location))
    updater.start_polling()
    updater.idle()


def main():
    start_bot()
