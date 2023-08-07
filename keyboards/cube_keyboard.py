from aiogram import types


def get_kb_accept_cube(user_id, bid):
    buttons = [types.InlineKeyboardButton(text="Принять участие",
                                          callback_data="accept_dice_" + str(user_id) + '_' + str(bid)), ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
