from aiogram.fsm.state import State, StatesGroup
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()
from asd.kb.keyboard import main_kb
from asd.kb.keyboard import check_kb
from asd.kb.keyboard import slovo_kb
from asd.kb.keyboard import cancel_kb

class StudyState(StatesGroup):
    waiting_for_next = State()
class CheckState(StatesGroup):
    waiting_for_text = State()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать в тренажёр английского!Выберите режим:", reply_markup=main_kb()
    )


@router.message(F.text == "Проверить текст")
async def start_check(message: Message, state: FSMContext):
    await message.answer(
        "Напишите текст на английском для проверки:",
        reply_markup=cancel_kb()
    )
    await state.set_state(CheckState.waiting_for_text)
