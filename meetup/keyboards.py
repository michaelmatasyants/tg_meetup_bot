from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder


speaker_button = KeyboardButton(text='Спикер')
guest_button = KeyboardButton(text='Гость мероприятия')

get_id_button = InlineKeyboardButton(text='Узнать свой telegram id',
                                     callback_data='get_id')
next_button = InlineKeyboardButton(text='Далее',
                                   callback_data='next')


role_selection_keyboard = ReplyKeyboardMarkup(
    keyboard=[[speaker_button], [guest_button]],
    resize_keyboard=True,
    one_time_keyboard=True)

kb_builder = InlineKeyboardBuilder()
get_id_keyboard = InlineKeyboardMarkup(inline_keyboard=[[get_id_button]])
next_keyboard = InlineKeyboardMarkup(inline_keyboard=[[next_button]])
