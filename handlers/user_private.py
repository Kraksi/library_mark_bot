from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from filters.chat_types import ChatTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.bot_test_db import check_db

from kbds.user_kbds import (
    get_auth_keyboard, 
    get_check_keyboard,
    get_buildings_keyboard,
    get_questions_keyboard,
    get_rating_keyboard,
    get_topics_keyboard
)

users_db = {}

class AuthStates(StatesGroup):
    surname = State()    # Ожидание фамилии
    name = State()       # Ожидание имени
    patronymic = State() # Ожидание отчества

    texts = {
        'AuthStates:surname':'Введите фамилию заново',
        'AuthStates:name':'Введите имя заново',
        'AuthStates:patronymic':'Введите отчество заново',
    }

class CheckStates(StatesGroup):
    building = State()  # Ожидание выбора здания
    topic = State()     # Ожидание выбора темы
    question = State()  # Ожидание выбора вопроса
    rating = State()    # Ожидание оценки

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

"""

Блок Авторизация пользователя в боте.

"""

@user_private_router.message(F.text == "/start")
async def cmd_start(message: types.Message):
    user_id = message.from_user.id

    # # Проверяем, авторизован ли пользователь
    # if user_id in users_db:
    #     # Если авторизован, показываем кнопку "Начать проверку"
    #     keyboard = get_check_keyboard()
    #     await message.answer("Вы авторизованы. Выберите действие:", reply_markup=keyboard)
    # else:
    #     # Если не авторизован, показываем кнопку "Авторизация"
    #     keyboard = get_auth_keyboard()
    #     await message.answer("Для начала работы необходимо авторизоваться:", reply_markup=keyboard)
    keyboard = get_check_keyboard()
    flag = check_db()
    if flag:
        await message.answer("Check True")
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

    if current_state == AuthStates.surname:
        await message.answer('Предидущего шага нет, или введите фамилию или напишите /отмена ')
        return
    
    previous = None
    for step in AuthStates.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к прошлому шагу \n {AuthStates.texts[previous.state]}")
            return
        previous = step

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

# Заглушка для базы данных
fake_db = {
    "buildings": [{"id": i, "address": f"Адрес {i}"} for i in range(1, 51)],
    "topics": [{"id": i, "name": f"Тема {i}"} for i in range(1, 6)],
    "questions": [{"id": i, "text": f"Вопрос {i}"} for i in range(1, 11)],
    "users": {
        131144684: {"id": 131144684, "surname": "Иванов", "name": "Иван", "patronymic": "Иванович"}  # Пример пользователя
    }
}

"""

Блок Проверка

"""

# Обработчик нажатия на кнопку "Начать проверку"
@user_private_router.callback_query(F.data == "check")
async def process_check(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    # Получаем данные пользователя из базы данных
    user_id = callback_query.from_user.id
    user_data = fake_db["users"].get(user_id)

    if not user_data:
        await callback_query.message.answer("Ошибка: пользователь не найден в базе данных.")
        return

    # Сохраняем ID и ФИО пользователя в состоянии FSM
    await state.update_data(
        user_id=user_data["id"],
        user_fullname=f"{user_data['surname']} {user_data['name']} {user_data['patronymic']}"
    )

    await callback_query.message.answer("Выберите здание:", reply_markup=get_buildings_keyboard(fake_db["buildings"]))
    await state.set_state(CheckStates.building)

# Обработчик выбора здания
@user_private_router.callback_query(CheckStates.building, F.data.startswith("building_"))
async def process_building(callback_query: types.CallbackQuery, state: FSMContext):
    building_id = int(callback_query.data.split("_")[1])
    await state.update_data(building_id=building_id)
    await callback_query.answer()
    await callback_query.message.answer("Выберите тему проверки:", reply_markup=get_topics_keyboard(fake_db["topics"]))
    await state.set_state(CheckStates.topic)

# Обработчик выбора темы
@user_private_router.callback_query(CheckStates.topic, F.data.startswith("topic_"))
async def process_topic(callback_query: types.CallbackQuery, state: FSMContext):
    topic_id = int(callback_query.data.split("_")[1])
    await state.update_data(topic_id=topic_id)
    await callback_query.answer()
    await callback_query.message.answer("Выберите вопрос:", reply_markup=get_questions_keyboard(fake_db["questions"]))
    await state.set_state(CheckStates.question)

# Обработчик выбора вопроса
@user_private_router.callback_query(CheckStates.question, F.data.startswith("question_"))
async def process_question(callback_query: types.CallbackQuery, state: FSMContext):
    question_id = int(callback_query.data.split("_")[1])
    await state.update_data(question_id=question_id)
    await callback_query.answer()
    await callback_query.message.answer("Поставьте оценку (от 0 до 2):", reply_markup=get_rating_keyboard())
    await state.set_state(CheckStates.rating)

# Обработчик выбора оценки
@user_private_router.callback_query(CheckStates.rating, F.data.startswith("rating_"))
async def process_rating(callback_query: types.CallbackQuery, state: FSMContext):
    rating = int(callback_query.data.split("_")[1])
    user_data = await state.get_data()
    await callback_query.answer()

    # Формируем результат проверки
    result = {
        "user_id": user_data["user_id"],  # ID пользователя
        "user_fullname": user_data["user_fullname"],  # ФИО пользователя
        "building_id": user_data["building_id"],
        "topic_id": user_data["topic_id"],
        "question_id": user_data["question_id"],
        "rating": rating
    }

    # Сохраняем результат проверки (заглушка)
    print("Результат проверки:", result)  # В реальном проекте сохраняем в БД

    await callback_query.message.answer("Спасибо! Проверка завершена.")
    await state.clear()

# Обработчик пагинации для зданий
@user_private_router.callback_query(F.data.startswith("buildings_page_"))
async def process_buildings_pagination(callback_query: types.CallbackQuery, state: FSMContext):
    page = int(callback_query.data.split("_")[2])
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=get_buildings_keyboard(fake_db["buildings"], page=page))




@user_private_router.message(or_f(Command('about'), (F.text.lower() == 'о боте')))
async def echo(message: types.Message):
    await message.answer("Информация о боте:")

@user_private_router.message(Command('adress'))
async def echo(message: types.Message):
    await message.answer("Список местоположений объектов:")

# @user_private_router.message(F.text)
# async def echo(message: types.Message):
#     await message.answer("Список местоположений объектов:")

