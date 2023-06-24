from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


speaker_button = KeyboardButton(text='Спикер')
guest_button = KeyboardButton(text='Гость мероприятия')
get_id_button = KeyboardButton(text='Узнать свой telegram id')
next_button = KeyboardButton(text='Далее')
home_button = KeyboardButton(text='Вернуться в начало')
contact_organizer_button = KeyboardButton(text='Написать организатору')
start_report_button = KeyboardButton(text='Начать доклад')
end_report_button = KeyboardButton(text='Завершить доклад')

role_selection_keyboard = ReplyKeyboardMarkup(
    keyboard=[[speaker_button], [guest_button]],
    resize_keyboard=True)

kb_builder = ReplyKeyboardBuilder()
get_id_keyboard = ReplyKeyboardMarkup(keyboard=[[get_id_button], [contact_organizer_button], [home_button]], resize_keyboard=True)
next_keyboard = ReplyKeyboardMarkup(keyboard=[[next_button], [contact_organizer_button], [home_button]], resize_keyboard=True)
start_report_keyboard = ReplyKeyboardMarkup(keyboard=[[start_report_button], [contact_organizer_button], [home_button]], resize_keyboard=True)
end_report_keyboard = ReplyKeyboardMarkup(keyboard=[[end_report_button]], resize_keyboard=True)
go_home_keyboard = ReplyKeyboardMarkup(keyboard=[[home_button], [contact_organizer_button]], resize_keyboard=True)
