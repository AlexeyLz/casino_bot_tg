import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Text

from misc import dp
from database.database_functions import check_user_registered, take_money, give_money, check_user_have_balance
from texts import you_are_not_registered_text
from constants import emoji_dice


@dp.callback_query_handler(Text(startswith="accept_dice"))
async def callbacks_num_start(call: types.CallbackQuery):
    call_data = call.data.split('_')
    id_sender = int(call_data[2])
    bid = float(call_data[3])
    bid_with_commission = round(bid * 0.95, 1)
    id_button_clicked = int(call['from']['id'])
    if not check_user_registered(id_button_clicked):
        await call.message.answer(you_are_not_registered_text)
        return
    if not check_user_have_balance(id_button_clicked, bid):
        await call.message.answer('У игрока 2 не хватает на балансе средств для данной игры.')
        return
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Игрок 1 кидает кубик...')
    result_sender = await call.message.answer_dice(emoji=emoji_dice)
    value_sender = int(result_sender.dice.value)
    await asyncio.sleep(5)
    await call.message.answer(f'Игроку 1 выпало {value_sender}\nИгрок 2 кидает кубик...')
    result_button_clicked = await call.message.answer_dice(emoji=emoji_dice)
    value_button_clicked = int(result_button_clicked.dice.value)
    await asyncio.sleep(5)
    await call.message.answer(f'Игроку 2 выпало {value_button_clicked}.')
    if value_sender > value_button_clicked:
        await call.message.answer(
            f'Победил игрок 1. Со счетом {value_sender}:{value_button_clicked}.'
            f'\nОн забирает себе {bid_with_commission} руб.')
        give_money(id_sender, bid_with_commission)
        take_money(id_button_clicked, bid)

    elif value_button_clicked > value_sender:
        await call.message.answer(
            f'Победил игрок 2. Со счетом {value_button_clicked}:{value_sender}.'
            f'\nОн забирает себе {bid_with_commission} руб.')
        give_money(id_button_clicked, bid_with_commission)
        take_money(id_sender, bid)
    else:
        await call.message.answer(f'Ничья. На кубиках выпало одинаковое число {value_sender}.')
    with open('logs.txt', 'a', encoding='UTF-8') as logs:
        game_text = f'Отправил: {id_sender}, принял: {id_button_clicked},' \
                    f' ставка: {bid}, кубики: {value_sender} - {value_button_clicked}\n'
        logs.write(game_text)
