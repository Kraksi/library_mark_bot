from aiogram import types, Router
from aiogram.filters import CommandStart, Command

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Привет')

@user_private_router.message(Command('about'))
async def echo(message: types.Message):
    await message.answer("Информация о боте:")

@user_private_router.message(Command('adress'))
async def echo(message: types.Message):
    await message.answer("Список местоположений объектов:")