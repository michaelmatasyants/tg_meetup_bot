from config import BOT_TOKEN
from keyboards import role_selection_keyboard
from texts import TEXTS

from aiogram import Bot, Router
from aiogram.types import Message
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


@router.message(StateFilter(default_state), Text(text='Спикер'))
async def speaker_greeting(message: Message, state: FSMContext):
    await message.answer(text=TEXTS['speaker_greeting'])
    await state.set_state(FSM.speaker_state)
