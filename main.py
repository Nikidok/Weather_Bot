import os
import datetime
import requests
import math  # Добавил импорт math
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from settings import *  # Убедись, что у тебя есть settings.py с BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города, и я пришлю сводку погоды")

@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        city_name = message.text.strip()  # Получаем название города от пользователя
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&units=metric&appid=b4e141d705f7bcd2dfa53f5b58583a7a")
        data = response.json()

        if data.get("cod") != 200:
            await message.reply("Город не найден! Проверьте правильность написания.")
            return

        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        # Рассчитываем восход, закат и продолжительность дня
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        code_to_smile = {
            "Clear": "Ясно ☀️",
            "Clouds": "Облачно ☁️",
            "Rain": "Дождь 🌧",
            "Drizzle": "Мелкий дождь 🌦",
            "Thunderstorm": "Гроза ⚡",
            "Snow": "Снег ❄",
            "Mist": "Туман 🌫"
        }

        weather_description = data["weather"][0]["main"]
        wd = code_to_smile.get(weather_description, "Посмотри в окно, я не понимаю, что там за погода...")

        await message.reply(
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Погода в городе: {city}\nТемпература: {cur_temp}°C {wd}\n"
            f"Влажность: {humidity}%\n"
            f"Давление: {math.ceil(pressure / 1.333)} мм.рт.ст\n"
            f"Ветер: {wind} м/с\n"
            f"Восход солнца: {sunrise_timestamp.strftime('%H:%M')}\n"
            f"Закат солнца: {sunset_timestamp.strftime('%H:%M')}\n"
            f"Продолжительность дня: {str(length_of_the_day).split('.')[0]}\n"
            f"Хорошего дня! 🌞"
        )

    except Exception as e:
        await message.reply("Ошибка! Проверьте название города.")
        print(f"Ошибка: {e}")  # Логируем ошибку в консоль для отладки

if __name__ == "__main__":
    executor.start_polling(dp)
