from aiogram import Bot, Dispatcher, types
import asyncio
from dotenv import find_dotenv, load_dotenv
import os
load_dotenv(find_dotenv())

from handlers.user_private import user_private_router
from common.bot_cmds_list import private


ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query', 'inline_query']

# Создание экземплояра бота
bot = Bot(token=os.getenv('TOKEN'))

# Создание экземпляра диспетчера для получения обновлений
dp = Dispatcher()

dp.include_router(user_private_router)

#Активация старта просулшки сервера
async def app():
    await bot.delete_webhook(drop_pending_updates=True)
    #await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(app())