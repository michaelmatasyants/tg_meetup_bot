from config import BOT_TOKEN
from keyboards import (role_selection_keyboard, get_id_keyboard, next_keyboard,
                       start_report_keyboard, end_report_keyboard,
                       go_home_keyboard, event_keyboard,
                       guest_registration_keyboard)
from keyboards import (homepage_button, event_homepage_button,
                       show_event_program_button)
from texts import TEXTS

from temporary_data import speakers, speakers_id, reports, event, event_program

from aiogram import Bot, Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import CommandStart, Text, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state



bot = Bot(BOT_TOKEN)
router = Router()


# TODO: здесь будут функции для запросов в бд
def get_speakers(Speaker):
    pass


class FSM(StatesGroup):
    speaker_state = State()
    guest_state = State()
    enter_email_state = State()
    enter_question_state = State()


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
    if message.from_user.id in speakers_id:
        await message.answer(text=TEXTS['speaker_greeting'].format(message.from_user.first_name),  # TODO здесь необходимо подтянуть имя спикера
                             reply_markup=next_keyboard)
        # await state.set_state(FSM.speaker_state)
    else:
        await message.answer(text=TEXTS['speaker_not_recognized'],
                             reply_markup=get_id_keyboard)


# @router.callback_query(StateFilter(default_state), Text(text='get_id'))
@router.message(Text(text='Узнать свой telegram id'))
async def process_get_id(message: Message):
    await message.answer(text=f'Ваш telegram id:\n{message.from_user.id}')


# @router.callback_query(StateFilter(FSM.speaker_state), Text(text='next'))
@router.message(Text(text='Далее'))
async def process_display_reports(message: Message):
    text = 'Выберите доклад из списка запланированных мероприятий, чтобы начать доклад или прочитать вопросы по докладу:\n'
    # запрос в БД для получения списка докладов
    kb_builder = ReplyKeyboardBuilder()
    for count, report in enumerate(reports, start=1):
        text += TEXTS['reports'].format(count, report['Тема доклада'], report['Дата и время'], report['Место проведения'])
    buttons = [KeyboardButton(text=f'№{count} {report["Тема доклада"]}') for count, report in enumerate(reports, start=1)]
    kb_builder.row(*buttons, width=1)
    kb_builder.row(homepage_button)
    await message.answer(text=text, reply_markup=kb_builder.as_markup(resize_keyboard=True))


@router.message(lambda msg: msg.text.startswith('№'))
async def process_report_selection(message: Message):
    for element in reports:
        if element['Тема доклада'] == message.text[3:]:
            report = element
    text = TEXTS['report'].format(report['Тема доклада'], report['Дата и время'], report['Место проведения'])
    await message.answer(text=text, reply_markup=start_report_keyboard)


@router.message(Text(text='Начать доклад'))
async def process_start_report(message: Message):
    # TODO запись в БД с временем начала
    await message.answer(text='Вы начали доклад. Когда доклад будет завершен, вы можете приступить к ответам на вопросы слушателей.',
                         reply_markup=end_report_keyboard)


@router.message(Text(text='Завершить доклад'))
async def process_end_report(message: Message):
    # TODO запись в БД с временем завершения доклада
    # TODO получить вопросы по докладу
    questions = '<Вопросы слушателей>'
    await message.answer(text=questions,
                         reply_markup=go_home_keyboard)


# ветка гостя
# @router.message(StateFilter(default_state, FSM.speaker_state), Text(text='Гость мероприятия'))
@router.message(Text(text='Гость мероприятия'))
async def process_guest_greeting(message: Message, state: FSMContext):
    await message.answer(text=TEXTS['guest_greeting'].format(message.from_user.first_name),
                         reply_markup=guest_registration_keyboard)
    # await state.set_state(FSM.guest_state)


@router.message(Text(text='Ввести Email'))
async def process_enter_email(message: Message, state: FSMContext):
    await message.answer(text='Спасибо за доверие. Мы честно не будем спамить.\nОтправьте нам ваш Email:',
                         reply_markup=go_home_keyboard)
    await state.set_state(FSM.enter_email_state)


@router.message(StateFilter(FSM.enter_email_state))
async def enter_mail(message: Message, state: FSMContext):
    email = message.text
    print('email:', email)
    await message.answer(text=TEXTS['success_registration'].format(event['topic'], event['date'], event['place'], event['time']),
                         reply_markup=event_keyboard)
    await state.set_state(default_state)


@router.message(Text(text=['Продолжить без Email', 'На главную']))
async def process_without_email(message: Message, state: FSMContext):
    await message.answer(text=TEXTS['success_registration'].format(event['topic'], event['date'], event['place'], event['time']),
                         reply_markup=event_keyboard)


@router.message(Text(text='Спикеры'))
async def process_show_speakers(message: Message, state: FSMContext):
    kb_builder = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text=speaker['name']) for speaker in speakers]
    kb_builder.row(*buttons, width=2)
    kb_builder.row(show_event_program_button)
    kb_builder.row(event_homepage_button)
    await message.answer(text=TEXTS['show_speakers'], reply_markup=kb_builder.as_markup(resize_keyboard=True))


@router.message(Text(text='Программа мероприятия'))
async def process_show_program(message: Message, state: FSMContext):
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.row(event_homepage_button)
    await message.answer(text=event_program,
                         reply_markup=kb_builder.as_markup(resize_keyboard=True))


@router.message(Text(text='Задать вопрос спикеру'))
async def process_ask_question(message: Message, state: FSMContext):
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.row(event_homepage_button)
    await message.answer(text='Чтобы задать вопрос спикеру, который сейчас читает доклад введите его ниже.\n\n<Спикер>\n<Тема доклада>',
                         reply_markup=kb_builder.as_markup(resize_keyboard=True))
    await state.set_state(FSM.enter_question_state)


@router.message(StateFilter(FSM.enter_question_state))
async def enter_question(message: Message, state: FSMContext):
    question = message.text
    print('question:', question)
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.row(event_homepage_button)
    await message.answer(text='Спасибо за вопрос.\nСпикер ответит на него после завершения доклада.',
                         reply_markup=kb_builder.as_markup(resize_keyboard=True))
    await state.set_state(default_state)


# process_start_command
# process_contact_organizer
# process_speaker_greeting
# process_get_id
# process_display_reports
# process_report_selection
# process_start_report
# process_end_report
# process_guest_greeting
# process_enter_email
# enter_mail
# process_process_without_email
# process_show_speakers
# process_show_program
# process_ask_question
# enter_question

# print(message.json(indent=4, exclude_none=True))
