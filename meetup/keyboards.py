from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)


speaker_button = KeyboardButton(text='Спикер')
guest_button = KeyboardButton(text='Гость мероприятия')

role_selection_keyboard = ReplyKeyboardMarkup(
    keyboard=[[speaker_button], [guest_button]], resize_keyboard=True)
