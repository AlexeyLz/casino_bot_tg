import asyncio
from aiogram.dispatcher.filters import Text

from database.database_functions import register_user
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from texts import pay_text, dice_error_command_text, dice_error_number_text, dice_input_bid_text, \
    cube_only_in_group_text, \
    cube_price_more_then_ten_text, cube_incorrect_input_text, you_are_not_registered_text
from constants import parse_mode, emoji_dice, group
from misc import dp
from keyboards.cube_keyboard import get_kb_accept_cube
from database.database_functions import check_user_registered, check_user_have_balance, give_money, get_balance
from callbacks import cube_callback


@dp.message_handler(commands=['pay'])
async def cmd_pay(message: types.Message):
    args = message.get_args()
    try:
        user_id = int(args.split()[0])
        summa = float(args.split()[1])
    except:
        await message.answer(pay_text, parse_mode=parse_mode)
        return
    if not check_user_registered(user_id):
        await message.answer('Данный пользователь не зарегистрирован.')
    give_money(user_id, summa)
    await message.answer('Перевод выполнен')


@dp.message_handler(commands=['dice'])
async def cmd_dice(message: types.Message):
    args = message.get_args()
    try:
        number = int(args.split()[0])
        bid = int(args.split()[1])
    except:
        await message.answer(dice_error_command_text, parse_mode=parse_mode)
        return
    if number < 1 or number > 6:
        await message.answer(dice_error_number_text)
        return
    elif bid < 50 or bid > 10000:
        await message.answer(dice_input_bid_text)
        return
    await message.answer(f'Ваша ставка: {bid}\nВаше число: {number}')
    dice_msg = await message.answer_dice(emoji=emoji_dice)
    await asyncio.sleep(5)
    if dice_msg.dice.value == number:
        await message.answer(f'Поздравляю с выигрышем!🥳\nВы выиграли {bid * 2}')
    else:
        await message.answer(f'К сожалению, вы проиграли.😔\nВыпало число: {dice_msg.dice.value}')


@dp.message_handler(commands=['cube'])
async def cmd_cube(message: types.Message):
    chat_type = message.chat.type
    if chat_type != group:
        await message.answer(cube_only_in_group_text)
        return
    if not check_user_registered(message.from_user.id):
        await message.answer(you_are_not_registered_text)
        return
    try:
        args = message.get_args()
        bid = int(args)
    except:
        await message.answer(cube_incorrect_input_text)
        return
    if bid < 10:
        await message.answer(cube_price_more_then_ten_text)
        return
    if not check_user_have_balance(message.from_user.id, bid):
        await message.answer('У вас не хватает средств на данную ставку.')
        return
    await message.answer(f'{message.from_user.username} предлагает сыграть в кости.\nСтавка: {bid}',
                         reply_markup=get_kb_accept_cube(message.from_user.id, bid))
