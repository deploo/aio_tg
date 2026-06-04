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
from asd.kb.keyboard import words



class StudyState(StatesGroup):
    word_index = State()
    learned = State()
class CheckState(StatesGroup):
    waiting_for_text = State()


@router.message(StateFilter(None), F.text == "Выучить 5 слов")
async def start_study(message: Message, state: FSMContext):
    await state.update_data(word_index=0, learned=0)
    await message.answer(
        f"Слово 1/5: apple - яблоко",
        reply_markup=slovo_kb()
    )
    await state.set_state(StudyState.word_index)



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


@router.message(CheckState.waiting_for_text, F.text)
async def check_text(message: Message, state: FSMContext):



    await message.answer(reply_markup=check_kb())
    await state.clear()


@router.message(CheckState.waiting_for_text)
async def check_incorrect(message: Message):
    await message.answer("Пожалуйста, отправьте текст для проверки.")
