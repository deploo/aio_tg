from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


words = ["apple", "cat", "dog", "house", "car"]


def main_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Выучить 5 слов"),
        KeyboardButton(text="Проверить текст"),
        KeyboardButton(text="Статистика"),
        KeyboardButton(text="Сбросить")
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def slovo_kb() -> InlineKeyboardMarkup:
    InlineKeyboardBuilder.button(text="Следующее слово", callback_data="next")
    InlineKeyboardBuilder.button(text="Пример", callback_data="example")
    InlineKeyboardBuilder.button(text="Запомнил", callback_data="remember")
    InlineKeyboardBuilder.button(text="Выйти", callback_data="exit")
    return InlineKeyboardBuilder.as_markup()


def check_kb() -> InlineKeyboardMarkup:
    InlineKeyboardBuilder.button(text="Проверить другой текст", callback_data="again")
    InlineKeyboardBuilder.button(text="Исправить ошибку", callback_data="fix")
    InlineKeyboardBuilder.button(text="Главное меню", callback_data="menu")
    return InlineKeyboardBuilder.as_markup()

def cancel_kb() -> ReplyKeyboardMarkup:
    ReplyKeyboardBuilder().add( KeyboardButton(text="Отмена"), KeyboardButton(text="Меню"))
    return ReplyKeyboardBuilder().as_markup(resize_keyboard=True)