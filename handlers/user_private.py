from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from filters.chat_types import ChatTypeFilter


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

@user_private_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Привет')

@user_private_router.message(or_f(Command('about'), (F.text.lower() == 'о боте')))
async def echo(message: types.Message):
    await message.answer("Информация о боте:")

@user_private_router.message(Command('adress'))
async def echo(message: types.Message):
    await message.answer("Список местоположений объектов:")

# @user_private_router.message(F.text)
# async def echo(message: types.Message):
#     await message.answer("Список местоположений объектов:")