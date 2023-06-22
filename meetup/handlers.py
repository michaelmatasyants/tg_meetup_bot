from config import BOT_TOKEN
from keyboards import (role_selection_keyboard, get_id_keyboard, next_keyboard,
                       kb_builder)
from texts import TEXTS

from temporary_data import speakers, reports

from aiogram import Bot, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
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
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=TEXTS['greeting'],
                         reply_markup=role_selection_keyboard)
    await state.set_state(default_state)


# ветка спикера
# @router.message(StateFilter(default_state), Text(text='Спикер'))
@router.message(Text(text='Спикер'))
async def speaker_greeting(message: Message, state: FSMContext):
    # TODO запрос в БД с данными о спикерах
    if message.from_user.id in speakers:
        await message.answer(text=TEXTS['speaker_greeting'].format(message.from_user.first_name),  # TODO здесь необходимо подтянуть имя спикера
                             reply_markup=next_keyboard)
        # await state.set_state(FSM.speaker_state)
    else:
        await message.answer(text=TEXTS['speaker_not_recognized'],
                             reply_markup=get_id_keyboard)


# @router.callback_query(StateFilter(default_state), Text(text='get_id'))
@router.callback_query(Text(text='get_id'))
async def get_id(callback: CallbackQuery):
    await callback.message.answer(
        text=f'Ваш telegram id:\n{callback.from_user.id}')


# @router.callback_query(StateFilter(FSM.speaker_state), Text(text='next'))
@router.callback_query(Text(text='next'))
async def display_reports(callback: CallbackQuery):
    text = 'Выберите доклад из списка запланированных мероприятий, чтобы начать доклад или прочитать вопросы по докладу:\n'
    # запрос в БД для получения списка докладов
    for report in reports:
        text += TEXTS['reports'].format(reports.index(report) + 1, report['Тема доклада'], report['Дата и время'], report['Место проведения'])
    buttons = [InlineKeyboardButton(text=report['Тема доклада'], callback_data=report['Тема доклада']) for report in reports]
    keyboard = kb_builder.row(*buttons, width=1)
    # await callback.answer()
    await callback.message.answer(text=text, reply_markup=keyboard.as_markup())


# print(callback.json(indent=4, exclude_none=True))
# ветка гостя
# @router.message(StateFilter(default_state, FSM.speaker_state), Text(text='Гость мероприятия'))
@router.message(Text(text='Гость мероприятия'))
async def guest_greeting(message: Message, state: FSMContext):
    if message.from_user.id in speakers:
        await message.answer(text=TEXTS['guest_greeting'].format(message.from_user.first_name))
        # await state.set_state(FSM.guest_state)


# print(callback.json(indent=4, exclude_none=True))
