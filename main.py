from aiogram import Bot, Dispatcher, types
import asyncio

# Создание экземплояра бота
bot = Bot(token="7887773449:AAGkbB2t4Ut97wsLnBaC7u8XXmYC8AKNGKg")

# Создание экземпляра диспетчера для получения обновлений
dp = Dispatcher()

@dp.message()
async def start(message: types.Message):
    await message.answer('Привет')

#Активация старта просулшки сервера
async def app():
    await dp.start_polling(bot)

asyncio.run(app())