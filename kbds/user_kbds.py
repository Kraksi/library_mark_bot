from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

def make_paginated_keyboard(items, prefix, page=0, per_page=5):
    start = page * per_page
    end = start + per_page
    current_items = items[start:end]
    buttons = [[InlineKeyboardButton(text=item.name, callback_data=f"{prefix}_{item.id}")] for item in current_items]
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"{prefix}_page_{page - 1}"))
    if end < len(items):
        nav_buttons.append(InlineKeyboardButton(text="➡️ Далее", callback_data=f"{prefix}_page_{page + 1}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Начать проверку", callback_data="start_check")]])

def cancel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 К темам", callback_data="cancel_to_topics")],
        [InlineKeyboardButton(text="🏠 К адресам", callback_data="cancel_to_addresses")]
    ])