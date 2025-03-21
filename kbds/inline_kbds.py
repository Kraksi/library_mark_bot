from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def buildings_keyboard(buildings, page: int = 0, per_page: int = 10):
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    # Сегментируем список зданий по страницам
    start = page * per_page
    end = start + per_page
    
    # Добавляем кнопки для каждого здания на текущей странице
    for building in buildings[start:end]:
        keyboard.add(InlineKeyboardButton(text=building.name, callback_data=f"building_{building.id}"))
    
    # Добавляем навигационные кнопки, если нужно
    if len(buildings) > per_page:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page-1}"))
        if end < len(buildings):
            nav_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"page_{page+1}"))
        keyboard.add(*nav_buttons)  # Добавляем все навигационные кнопки в клавиатуру
    
    return keyboard

async def topics_keyboard(topics):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for topic in topics:
        keyboard.add(InlineKeyboardButton(text=topic.name, callback_data=f"topic_{topic.id}"))
    keyboard.add(InlineKeyboardButton(text="🔙 Вернуться к выбору здания", callback_data="back_to_buildings"))
    return keyboard

async def question_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.row(
        InlineKeyboardButton(text="0", callback_data="score_0"),
        InlineKeyboardButton(text="1", callback_data="score_1"),
        InlineKeyboardButton(text="2", callback_data="score_2")
    )
    return keyboard