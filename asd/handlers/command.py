from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from asd.kb.keyboard import main_kb ,  slovo_kb , check_kb, cancel_kb
from asd.datasourse.datebase import generate_new_word, check_llama

router = Router()


class StudyState(StatesGroup):
    waiting_for_next = State()


class CheckState(StatesGroup):
    waiting_for_text = State()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Добро пожаловать в тренажёр английского с AI!\nВыберите режим:",
        reply_markup=main_kb()
    )


@router.message(F.text == "Выучить 5 слов")
async def start_study(message: Message, state: FSMContext):
    await state.clear()

    loading_msg = await message.answer("Генерирую слова через AI...")

    words = []
    for i in range(5):
        word_data = await generate_new_word()
        words.append(word_data)

    await loading_msg.delete()

    await state.update_data(
        words=words,
        index=0,
        learned=0
    )

    data = await state.get_data()
    current_word = data["words"][0]

    await message.answer(
        text=f"Слово 1/5: {current_word['word']} - {current_word['trans']}",
        reply_markup=slovo_kb()
    )
    await state.set_state(StudyState.waiting_for_next)


@router.callback_query(StudyState.waiting_for_next)
async def study_actions(callback: CallbackQuery, state: FSMContext):
    action = callback.data
    data = await state.get_data()

    words = data.get("words", [])
    if not words:
        await callback.message.edit_text("Ошибка. Начните заново: /start")
        await state.clear()
        await callback.answer()
        return

    index = data.get("index", 0)
    learned = data.get("learned", 0)
    current_word = words[index]

    if action == "next":
        if index + 1 < len(words):
            await state.update_data(index=index + 1)
            next_word = words[index + 1]
            await callback.message.edit_text(
                text=f"Слово {index + 2}/{len(words)}: {next_word['word']} - {next_word['trans']}",
                reply_markup=slovo_kb()
            )
        else:
            await callback.message.edit_text(
                text=f"Поздравляю! Выучено слов: {learned}/5",
                reply_markup=None
            )
            await state.clear()
            await callback.message.answer(
                text="Главное меню:",
                reply_markup=main_kb()
            )

    elif action == "example":
        await callback.answer()
        await callback.message.answer(
            text=f"Пример: {current_word['example']}"
        )

    elif action == "remember":
        await state.update_data(learned=learned + 1)
        await callback.answer("Слово запомнено!")

    elif action == "exit":
        await callback.message.edit_text(
            text="Вы вышли из обучения.",
            reply_markup=None
        )
        await state.clear()
        await callback.message.answer(
            text="Главное меню:",
            reply_markup=main_kb()
        )

    await callback.answer()


@router.message(F.text == "Проверить текст")
async def start_check(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Напишите текст на английском для проверки:",
        reply_markup=cancel_kb()
    )
    await state.set_state(CheckState.waiting_for_text)


@router.message(CheckState.waiting_for_text, F.text)
async def check_text(message: Message, state: FSMContext):
    if message.text in ["Отмена", "Меню"]:
        await state.clear()
        await message.answer(
            text="Проверка отменена.",
            reply_markup=main_kb()
        )
        return

    user_text = message.text

    processing_msg = await message.answer("Проверяю текст через AI")

    response = await check_llama(user_text)

    await processing_msg.delete()

    await message.answer(
        text=f"Результат проверки:\n\n{response}",
        reply_markup=check_kb()
    )
    await state.clear()


@router.callback_query(F.data.in_(["again", "fix", "menu"]))
async def check_actions(callback: CallbackQuery, state: FSMContext):
    action = callback.data

    if action == "again":
        await callback.message.answer(
            text="Напишите другой текст:",
            reply_markup=cancel_kb()
        )
        await state.set_state(CheckState.waiting_for_text)
        await callback.message.delete()

    elif action == "fix":
        await callback.answer("Исправление скоро появится")

    elif action == "menu":
        await callback.message.edit_text(
            text="Главное меню:",
            reply_markup=None
        )
        await callback.message.answer(
            text="Выберите режим:",
            reply_markup=main_kb()
        )

    await callback.answer()


@router.message(F.text == "Статистика")
async def show_stats(message: Message, state: FSMContext):
    data = await state.get_data()
    learned = data.get("learned", 0)
    if learned > 0:
        await message.answer(
            text=f"Выучено слов в текущей сессии: {learned}/5"
        )
    else:
        await message.answer(
            text="Нет активной сессии."
        )


@router.message(F.text == "Сбросить")
async def reset_study(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Прогресс сброшен.",
        reply_markup=main_kb()
    )


@router.message()
async def unknown_message(message: Message):
    await message.answer(
        text="Используйте кнопки меню.",
        reply_markup=main_kb()
    )