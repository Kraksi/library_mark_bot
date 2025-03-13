from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def get_auth_keyboard():
    """
    Клавиатура с кнопкой "Авторизация".
    """
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Авторизация", callback_data="auth"))
    return builder.as_markup()

def get_check_keyboard():
    """
    Клавиатура с кнопкой "Начать проверку".
    """
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Начать проверку", callback_data="check"))
    return builder.as_markup()