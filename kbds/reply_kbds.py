from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def navigation_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        KeyboardButton("🔙 Назад"),
        KeyboardButton("⏩ Пропустить вопрос")
    )
    keyboard.row(
        KeyboardButton("🔙 Назад к выбору темы"),
        KeyboardButton("✅ Завершить проверку")
    )
    return keyboard
