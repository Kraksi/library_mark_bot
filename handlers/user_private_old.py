# from aiogram import types, Router, F
# from aiogram.filters import CommandStart, Command, or_f
# from filters.chat_types import ChatTypeFilter
# from aiogram.fsm.context import FSMContext
# from handlers.user_states import AuthStates, CheckStates
# #from database.bot_test_db import check_db
# from database.database_sqllite import get_user, get_buildings_with_unfinished_topics, get_topics_with_unfinished_questions, get_first_unfinished_question, save_result
# from database.engine_sqllite import get_session
# from kbds.inline_kbds import buildings_keyboard, topics_keyboard, question_keyboard
# from kbds.reply_kbds import navigation_keyboard
# from aiogram.fsm.state import State, StatesGroup

# from kbds.user_kbds import (
#     get_auth_keyboard, 
#     get_check_keyboard,
#     get_buildings_keyboard,
#     get_questions_keyboard,
#     get_rating_keyboard,
#     get_topics_keyboard
# )

# users_db = {}

# user_private_router = Router()
# user_private_router.message.filter(ChatTypeFilter(['private']))

# class UserFSM(StatesGroup):
#     selecting_building = State()
#     selecting_topic = State()
#     answering_question = State()
# """

# Блок Авторизация пользователя в боте.

# """

# @user_private_router.message(F.text == "/start")
# async def cmd_start(message: types.Message):
#     user_id = message.from_user.id

#     # Проверяем, авторизован ли пользователь
#     if user_id in users_db:
#         # Если авторизован, показываем кнопку "Начать проверку"
#         keyboard = get_check_keyboard()
#         await message.answer("Вы авторизованы. Выберите действие:", reply_markup=keyboard)
#     else:
#         # Если не авторизован, показываем кнопку "Авторизация"
#         keyboard = get_auth_keyboard()
#         await message.answer("Для начала работы необходимо авторизоваться:", reply_markup=keyboard)


# # Обработчик команды /cancel для отмены текущего процесса
# @user_private_router.message(F.text == "/cancel")
# async def cmd_cancel(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is None:
#         await message.answer("Нет активного процесса для отмены.")
#         return

#     await state.clear()
#     await message.answer("Процесс отменен.")

# # Обработчик команды /back для возврата на предыдущий шаг
# @user_private_router.message(F.text == "/back")
# async def cmd_back(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()

#     if current_state == AuthStates.surname:
#         await message.answer('Предидущего шага нет, или введите фамилию или напишите /отмена ')
#         return
    
#     previous = None
#     for step in AuthStates.__all_states__:
#         if step.state == current_state:
#             await state.set_state(previous)
#             await message.answer(f"Вы вернулись к прошлому шагу \n {AuthStates.texts[previous.state]}")
#             return
#         previous = step

# # Обработчик нажатия на кнопку "Авторизация"
# @user_private_router.callback_query(F.data == "auth")
# async def process_auth(callback_query: types.CallbackQuery, state: FSMContext):
#     await callback_query.answer()
#     await callback_query.message.answer("Введите вашу фамилию:")
#     await state.set_state(AuthStates.surname)

# # Обработчик ввода фамилии
# @user_private_router.message(AuthStates.surname)
# async def process_surname(message: types.Message, state: FSMContext):
#     await state.update_data(surname=message.text)
#     await message.answer("Введите ваше имя:")
#     await state.set_state(AuthStates.name)

# # Обработчик ввода имени
# @user_private_router.message(AuthStates.name)
# async def process_name(message: types.Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer("Введите ваше отчество:")
#     await state.set_state(AuthStates.patronymic)

# # Обработчик ввода отчества
# @user_private_router.message(AuthStates.patronymic)
# async def process_patronymic(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
#     user_data = await state.get_data()

#     # Сохраняем данные пользователя в "базу данных"
#     users_db[user_id] = {
#         "surname": user_data["surname"],
#         "name": user_data["name"],
#         "patronymic": user_data["patronymic"]
#     }

#     await message.answer(
#         f"Спасибо, {user_data['surname']} {user_data['name']} {user_data['patronymic']}, вы авторизованы!"
#     )
#     await state.clear()

#     # После авторизации показываем кнопку "Начать проверку"
#     keyboard = get_check_keyboard()
#     await message.answer("Теперь вы можете начать проверку:", reply_markup=keyboard)


# """

# Блок Проверка

# """

# # Обработчик нажатия на кнопку "Начать проверку"
# @user_private_router.callback_query(F.data == "check")
# async def process_check(callback: types.CallbackQuery, state: FSMContext):
#     async with get_session() as session:
#         user = await get_user(session, callback.message.from_user.id)
#         if not user:
#             await callback.message.answer("Вы не зарегистрированы.")
#             return
        
#         await state.update_data(user_id=user.id)
#         buildings = await get_buildings_with_unfinished_topics(session, user.id)
#         if not buildings:
#             await callback.message.answer("Нет доступных зданий.")
#             return
        
#         await callback.message.answer("Выберите здание:", reply_markup=await buildings_keyboard(buildings))
#         await state.set_state(UserFSM.selecting_building)

# @user_private_router.callback_query(lambda c: c.data.startswith("building_"), UserFSM.selecting_building)
# async def building_selected(callback: types.CallbackQuery, state: FSMContext):
#     async with get_session() as session:
#         building_id = int(callback.data.split('_')[1])
#         data = await state.get_data()
#         topics = await get_topics_with_unfinished_questions(session, data['user_id'], building_id)
        
#         if not topics:
#             await callback.message.answer("Нет доступных тем.")
#             return
        
#         await state.update_data(building_id=building_id)
#         await callback.message.answer("Выберите тему:", reply_markup=await topics_keyboard(topics))
#         await state.set_state(UserFSM.selecting_topic)

# @user_private_router.callback_query(lambda c: c.data.startswith("topic_"), UserFSM.selecting_topic)
# async def topic_selected(callback: types.CallbackQuery, state: FSMContext):
#     async with get_session() as session:
#         topic_id = int(callback.data.split('_')[1])
#         data = await state.get_data()
#         question = await get_first_unfinished_question(session, data['user_id'], topic_id)
        
#         if not question:
#             await callback.message.answer("Нет доступных вопросов.")
#             return
        
#         await state.update_data(topic_id=topic_id, question_id=question.id)
#         await callback.message.answer(question.text, reply_markup=question_keyboard())
#         await callback.message.answer("Выберите оценку:", reply_markup=navigation_keyboard())
#         await state.set_state(UserFSM.answering_question)

# @user_private_router.callback_query(lambda c: c.data.startswith("score_"), UserFSM.answering_question)
# async def process_answer(callback: types.CallbackQuery, state: FSMContext):
#     score = int(callback.data.split('_')[1])
#     async with get_session() as session:
#         data = await state.get_data()
#         await save_result(session, data['user_id'], data['building_id'], data['topic_id'], data['question_id'], score)
        
#         next_question = await get_first_unfinished_question(session, data['user_id'], data['topic_id'])
#         if next_question:
#             await state.update_data(question_id=next_question.id)
#             await callback.message.answer(next_question.text, reply_markup=question_keyboard())
#         else:
#             await callback.message.answer("Вы завершили тему. Выберите действие:", reply_markup=await topics_keyboard([]))
#             await state.set_state(UserFSM.selecting_topic)



