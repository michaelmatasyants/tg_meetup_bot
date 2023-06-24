from config import BOT_TOKEN
from keyboards import (role_selection_keyboard, get_id_keyboard, next_keyboard,
                       kb_builder, home_button, start_report_keyboard,
                       end_report_keyboard, go_home_keyboard)
from texts import TEXTS

from temporary_data import speakers, reports

from aiogram import Bot, Router
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import CommandStart, Text, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state


storage = MemoryStorage()
bot = Bot(BOT_TOKEN)
router = Router()


# TODO: здесь будут функции для запросов в бд
def get_speakers(Speaker):
    pass


class FSM(StatesGroup):
    speaker_state = State()
    guest_state = State()


@router.message(CommandStart())
@router.message(Text(text='Вернуться в начало'))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=TEXTS['greeting'],
                         reply_markup=role_selection_keyboard)
    await state.set_state(default_state)


@router.message(Text(text='Написать организатору'))
async def process_contact_organizer(message: Message, state: FSMContext):
    await message.answer(text='<Контакты организатора>')


# ветка спикера
# @router.message(StateFilter(default_state), Text(text='Спикер'))
@router.message(Text(text='Спикер'))
async def process_speaker_greeting(message: Message, state: FSMContext):
    # TODO запрос в БД с данными о спикерах
    if message.from_user.id in speakers:
        await message.answer(text=TEXTS['speaker_greeting'].format(message.from_user.first_name),  # TODO здесь необходимо подтянуть имя спикера
                             reply_markup=next_keyboard)
        # await state.set_state(FSM.speaker_state)
    else:
        await message.answer(text=TEXTS['speaker_not_recognized'],
                             reply_markup=get_id_keyboard)


# @router.callback_query(StateFilter(default_state), Text(text='get_id'))
@router.message(Text(text='Узнать свой telegram id'))
async def get_id(message: Message):
    await message.answer(text=f'Ваш telegram id:\n{message.from_user.id}')


# @router.callback_query(StateFilter(FSM.speaker_state), Text(text='next'))
@router.message(Text(text='Далее'))
async def display_reports(message: Message):
    text = 'Выберите доклад из списка запланированных мероприятий, чтобы начать доклад или прочитать вопросы по докладу:\n'
    # запрос в БД для получения списка докладов
    kb_builder = ReplyKeyboardBuilder()
    for count, report in enumerate(reports, start=1):
        text += TEXTS['reports'].format(count, report['Тема доклада'], report['Дата и время'], report['Место проведения'])
    buttons = [KeyboardButton(text=f'№{count} {report["Тема доклада"]}') for count, report in enumerate(reports, start=1)]
    kb_builder.row(*buttons, width=1)
    kb_builder.row(home_button)
    await message.answer(text=text, reply_markup=kb_builder.as_markup(resize_keyboard=True))


@router.message(lambda msg: msg.text.startswith('№'))
async def process_report_selection(message: Message):
    for element in reports:
        if element['Тема доклада'] == message.text[3:]:
            report = element
    text = TEXTS['report'].format(report['Тема доклада'], report['Дата и время'], report['Место проведения'])
    await message.answer(text=text, reply_markup=start_report_keyboard)


@router.message(Text(text='Начать доклад'))
async def start_report(message: Message):
    # TODO запись в БД с временем начала
    await message.answer(text='Вы начали доклад. Когда доклад будет завершен, вы можете приступить к ответам на вопросы слушателей.',
                         reply_markup=end_report_keyboard)


@router.message(Text(text='Завершить доклад'))
async def end_report(message: Message):
    # TODO запись в БД с временем завершения доклада
    # TODO получить вопросы по докладу
    # questions =
    await message.answer(text='<Вопросы слушателей>',
                         reply_markup=go_home_keyboard)


# print(callback.json(indent=4, exclude_none=True))
# ветка гостя
# @router.message(StateFilter(default_state, FSM.speaker_state), Text(text='Гость мероприятия'))
@router.message(Text(text='Гость мероприятия'))
async def guest_greeting(message: Message, state: FSMContext):
    if message.from_user.id in speakers:
        await message.answer(text=TEXTS['guest_greeting'].format(message.from_user.first_name))
        # await state.set_state(FSM.guest_state)


# print(callback.json(indent=4, exclude_none=True))
