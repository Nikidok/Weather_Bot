import os
import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from settings import *

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])  # ✅ Исправлено
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города, и я пришлю сводку погоды")

if __name__ == "__main__":
    executor.start_polling(dp)
