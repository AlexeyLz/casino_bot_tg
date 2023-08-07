import logging
import asyncio
from database.database_functions import register_user
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from misc import dp, bot
from handlers import help_commands, user_commands


class Form(StatesGroup):
    number = State()
    bid = State()


@dp.message_handler(commands=['game'])
async def game(message: types.Message, state: FSMContext):
    args = message.get_args().split()
    my_name = message.from_user.username
    my_id = message.from_user.id
    rival_id = args[0]
    bid = args[1]

    await message.answer('Вы отправили приглашение на игру пользователю')
    await bot.send_message(int(rival_id),
                           text=f'Вам пришло приглашение бросить кости от пользователя {my_id} [{my_name}]'
                                f'\nСтавка {bid}'
                                f'\n/accept{my_id} - принять'
                                f'\n/decline{my_id} - отклонить')

    # state_with: FSMContext = dp.current_state(chat=user_id, user=user_id)
    # await state_with.set_state('kek')
    # await state_with.reset_state()
    # current_state = await state_with.get_state()
    # print(current_state)


@dp.message_handler()
async def echo(message: types.Message):
    if message.text.startswith('/accept'):
        dice_emoji = '🎲'
        my_id = message.from_user.id
        my_name = message.from_user.username
        rival_id = int(message.text[7:])
        await message.reply(f"Вы приняли запрос от {rival_id}\nБросаем кубики...")
        await bot.send_message(rival_id, f'Соперник {my_id} [{my_name}] принял запрос бросить кубики')
        rival_dice_result = await bot.send_dice(rival_id, emoji=dice_emoji)
        my_dice_result = await message.answer_dice(emoji=dice_emoji)
        await asyncio.sleep(5)
        if rival_dice_result > my_dice_result:
            pass

        return
    await message.answer("Не понимаю тебя, вот тебе помощь")

    # dice_result = await message.answer_dice('🎲')
    # result = await bot.send_dice(message.chat.id, emoji='🎯')
    # print(result)


if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
        except Exception as e:
            print('Error found', e)
