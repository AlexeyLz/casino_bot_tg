from database.database_functions import register_user, get_balance
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from texts import start_text, games_text, balance_text
from constants import parse_mode
from misc import dp


@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    register_user(message)
    await message.answer(start_text, parse_mode=parse_mode)


@dp.message_handler(commands=['games'])
async def cmd_games(message: types.Message):
    await message.answer(games_text, parse_mode=parse_mode)


@dp.message_handler(commands=['balance'])
async def cmd_balance(message: types.Message):
    balance = get_balance(message.from_user.id)
    await message.answer(f'Ваш баланс: {balance} руб.')


@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'Ваш id: {message.from_user.id}')
