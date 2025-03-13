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

def get_buildings_keyboard(buildings: list, page: int = 0, page_size: int = 5):
    """
    Клавиатура с адресами зданий (с пагинацией).
    :param buildings: Список зданий.
    :param page: Текущая страница.
    :param page_size: Количество зданий на странице.
    """
    builder = InlineKeyboardBuilder()

    # Добавляем кнопки с адресами зданий
    for building in buildings[page * page_size:(page + 1) * page_size]:
        builder.add(InlineKeyboardButton(text=building["address"], callback_data=f"building_{building['id']}"))

    # Добавляем кнопки пагинации
    if page > 0:
        builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"buildings_page_{page - 1}"))
    if (page + 1) * page_size < len(buildings):
        builder.add(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"buildings_page_{page + 1}"))

    builder.adjust(1)  # Одна кнопка на строку
    return builder.as_markup()

def get_topics_keyboard(topics: list):
    """
    Клавиатура с темами проверки.
    """
    builder = InlineKeyboardBuilder()
    for topic in topics:
        builder.add(InlineKeyboardButton(text=topic["name"], callback_data=f"topic_{topic['id']}"))
    builder.adjust(1)  # Одна кнопка на строку
    return builder.as_markup()

def get_questions_keyboard(questions: list):
    """
    Клавиатура с вопросами.
    """
    builder = InlineKeyboardBuilder()
    for question in questions:
        builder.add(InlineKeyboardButton(text=question["text"], callback_data=f"question_{question['id']}"))
    builder.adjust(1)  # Одна кнопка на строку
    return builder.as_markup()

def get_rating_keyboard():
    """
    Клавиатура для оценки (от 0 до 2).
    """
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="0", callback_data="rating_0"),
        InlineKeyboardButton(text="1", callback_data="rating_1"),
        InlineKeyboardButton(text="2", callback_data="rating_2")
    )
    return builder.as_markup()