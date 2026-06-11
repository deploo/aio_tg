from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


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
    builder = InlineKeyboardBuilder()
    builder.button(text="Следующее слово", callback_data="next")  # <- вызываем метод ЭКЗЕМПЛЯРА
    builder.button(text="Пример", callback_data="example")
    builder.button(text="Запомнил", callback_data="remember")
    builder.button(text="Выйти", callback_data="exit")
    builder.adjust(2)
    return builder.as_markup()


def check_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Проверить другой текст", callback_data="again")
    builder.button(text="Исправить ошибку", callback_data="fix")
    builder.button(text="Главное меню", callback_data="menu")
    builder.adjust(1)
    return builder.as_markup()


def cancel_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Отмена"),
        KeyboardButton(text="Меню")
    )
    return builder.as_markup(resize_keyboard=True)