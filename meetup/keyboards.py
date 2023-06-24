from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


speaker_button = KeyboardButton(text='Спикер')
guest_button = KeyboardButton(text='Гость мероприятия')
get_id_button = KeyboardButton(text='Узнать свой telegram id')
next_button = KeyboardButton(text='Далее')
homepage_button = KeyboardButton(text='Вернуться в начало')
contact_organizer_button = KeyboardButton(text='Написать организатору')
start_report_button = KeyboardButton(text='Начать доклад')
end_report_button = KeyboardButton(text='Завершить доклад')
enter_email_button = KeyboardButton(text='Ввести Email')
without_email_button = KeyboardButton(text='Продолжить без Email')
show_speakers_button = KeyboardButton(text='Спикеры')
show_event_program_button = KeyboardButton(text='Программа мероприятия')
ask_speaker_button = KeyboardButton(text='Задать вопрос спикеру')
event_homepage_button = KeyboardButton(text='На главную')

role_selection_keyboard = ReplyKeyboardMarkup(keyboard=[[speaker_button], [guest_button]], resize_keyboard=True)
get_id_keyboard = ReplyKeyboardMarkup(keyboard=[[get_id_button], [contact_organizer_button], [homepage_button]], resize_keyboard=True)
next_keyboard = ReplyKeyboardMarkup(keyboard=[[next_button], [contact_organizer_button], [homepage_button]], resize_keyboard=True)
start_report_keyboard = ReplyKeyboardMarkup(keyboard=[[start_report_button], [contact_organizer_button], [homepage_button]], resize_keyboard=True)
end_report_keyboard = ReplyKeyboardMarkup(keyboard=[[end_report_button]], resize_keyboard=True)
go_home_keyboard = ReplyKeyboardMarkup(keyboard=[[homepage_button]], resize_keyboard=True)
guest_registration_keyboard = ReplyKeyboardMarkup(keyboard=[[enter_email_button], [without_email_button], [homepage_button]], resize_keyboard=True)
event_keyboard = ReplyKeyboardMarkup(keyboard=[[show_speakers_button], [show_event_program_button], [ask_speaker_button], [homepage_button]], resize_keyboard=True)
