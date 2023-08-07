import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


API_TOKEN = '6010248173:AAH_qaFFV4MdAwH4UN4c0dBnQ163nhl3FY4' #можно спрятать в .env

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())