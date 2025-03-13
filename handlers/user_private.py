from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from filters.chat_types import ChatTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from kbds.user_kbds import get_auth_keyboard, get_check_keyboard

users_db = {}

class AuthStates(StatesGroup):
    surname = State()
    name = State()
    patronymic = State()


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

@user_private_router.message(F.text == "/start")
async def cmd_start(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, авторизован ли пользователь
    if user_id in users_db:
        # Если авторизован, показываем кнопку "Начать проверку"
        keyboard = get_check_keyboard()
        await message.answer("Вы авторизованы. Выберите действие:", reply_markup=keyboard)
    else:
        # Если не авторизован, показываем кнопку "Авторизация"
        keyboard = get_auth_keyboard()
        await message.answer("Для начала работы необходимо авторизоваться:", reply_markup=keyboard)

# Обработчик нажатия на кнопку "Авторизация"
@user_private_router.callback_query(F.data == "auth")
async def process_auth(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("Введите вашу фамилию:")
    await state.set_state(AuthStates.surname)

# Обработчик ввода фамилии
@user_private_router.message(AuthStates.surname)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Введите ваше имя:")
    await state.set_state(AuthStates.name)

# Обработчик ввода имени
@user_private_router.message(AuthStates.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваше отчество:")
    await state.set_state(AuthStates.patronymic)

# Обработчик ввода отчества
@user_private_router.message(AuthStates.patronymic)
async def process_patronymic(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await state.get_data()

    # Сохраняем данные пользователя в "базу данных"
    users_db[user_id] = {
        "surname": user_data["surname"],
        "name": user_data["name"],
        "patronymic": user_data["patronymic"]
    }

    await message.answer(
        f"Спасибо, {user_data['surname']} {user_data['name']} {user_data['patronymic']}, вы авторизованы!"
    )
    await state.clear()

    # После авторизации показываем кнопку "Начать проверку"
    keyboard = get_check_keyboard()
    await message.answer("Теперь вы можете начать проверку:", reply_markup=keyboard)


# Обработчик команды /cancel для отмены текущего процесса
@user_private_router.message(F.text == "/cancel")
async def cmd_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нет активного процесса для отмены.")
        return

    await state.clear()
    await message.answer("Процесс отменен.")

# Обработчик команды /back для возврата на предыдущий шаг
@user_private_router.message(F.text == "/back")
async def cmd_back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == AuthStates.name:
        await state.set_state(AuthStates.surname)
        await message.answer("Введите вашу фамилию:")
    elif current_state == AuthStates.patronymic:
        await state.set_state(AuthStates.name)
        await message.answer("Введите ваше имя:")
    # elif current_state == CheckStates.waiting_for_topic:
    #     await message.answer("Выберите тему:")
    else:
        await message.answer("Невозможно вернуться назад.")



@user_private_router.message(or_f(Command('about'), (F.text.lower() == 'о боте')))
async def echo(message: types.Message):
    await message.answer("Информация о боте:")

@user_private_router.message(Command('adress'))
async def echo(message: types.Message):
    await message.answer("Список местоположений объектов:")

# @user_private_router.message(F.text)
# async def echo(message: types.Message):
#     await message.answer("Список местоположений объектов:")

