from handlers.user_states import RegisterState, SurveyState
from database.database_sqlite import user_exists, get_available_addresses, get_topics_by_address, get_unanswered_questions, get_user_id, export_answers_to_excel, save_answer
from kbds.user_kbds import start_keyboard, cancel_keyboard, make_paginated_keyboard
from database.engine_sqlite import session
from database.models_sqlite import User, Answer, Question, Address
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from filters.chat_types import ChatTypeFilter

ADMIN_IDS = [131144684]
user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

@user_private_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    if user_exists(message.from_user.id):
        await message.answer("Вы уже зарегистрированы.", reply_markup=start_keyboard())
    else:
        await message.answer("Введите вашу фамилию:")
        await state.set_state(RegisterState.last_name)

@user_private_router.message(RegisterState.last_name)
async def reg_last(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Имя:")
    await state.set_state(RegisterState.first_name)

@user_private_router.message(RegisterState.first_name)
async def reg_first(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Отчество:")
    await state.set_state(RegisterState.middle_name)

@user_private_router.message(RegisterState.middle_name)
async def reg_done(message: Message, state: FSMContext):
    data = await state.get_data()
    user = User(telegram_id=message.from_user.id,
                last_name=data['last_name'],
                first_name=data['first_name'],
                middle_name=message.text)
    session.add(user)
    session.commit()
    await state.clear()
    await message.answer("Регистрация завершена!", reply_markup=start_keyboard())

@user_private_router.callback_query(F.data == "start_check")
async def start_check(callback: CallbackQuery, state: FSMContext):
    user_id = get_user_id(callback.from_user.id)
    addresses = get_available_addresses(user_id)
    if addresses:
        await state.set_state(SurveyState.choosing_address)
        await state.update_data(addresses=addresses)
        await callback.message.answer("Выберите адрес:", reply_markup=make_paginated_keyboard(addresses, "address", 0))
    else:
        await callback.message.answer("Вы уже прошли проверку по всем адресам.")

@user_private_router.callback_query(F.data.startswith("address_page_"))
async def paginate_address(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split("_")[-1])
    data = await state.get_data()
    addresses = data.get("addresses", [])
    await callback.message.edit_reply_markup(reply_markup=make_paginated_keyboard(addresses, "address", page))

@user_private_router.callback_query(F.data.startswith("address_"))
async def choose_address(callback: CallbackQuery, state: FSMContext):
    address_id = int(callback.data.split("_")[1])
    await state.update_data(address_id=address_id)
    user_id = get_user_id(callback.from_user.id)
    topics = get_topics_by_address(address_id, user_id)
    if topics:
        await state.set_state(SurveyState.choosing_topic)
        await state.update_data(topics=topics)
        await callback.message.answer("Выберите тему:", reply_markup=make_paginated_keyboard(topics, "topic", 0))
    else:
        await callback.message.answer("Вы прошли все темы по данному адресу.")

@user_private_router.callback_query(F.data.startswith("topic_page_"))
async def paginate_topic(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split("_")[-1])
    data = await state.get_data()
    topics = data.get("topics", [])
    await callback.message.edit_reply_markup(reply_markup=make_paginated_keyboard(topics, "topic", page))

@user_private_router.callback_query(F.data.startswith("topic_"))
async def choose_topic(callback: CallbackQuery, state: FSMContext):
    topic_id = int(callback.data.split("_")[1])
    user_id = get_user_id(callback.from_user.id)
    questions = get_unanswered_questions(topic_id, user_id)
    if questions:
        await state.set_state(SurveyState.answering_questions)
        await state.update_data(topic_id=topic_id, questions=[(q.id, q.question) for q in questions], q_index=0)
        await callback.message.answer(questions[0].question, reply_markup=cancel_keyboard())
    else:
        await callback.message.answer("Все вопросы по этой теме уже пройдены.")


@user_private_router.callback_query(F.data == "cancel_to_topics")
async def cancel_to_topics(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    topics = data.get("topics", [])
    if topics:
        await state.set_state(SurveyState.choosing_topic)
        await callback.message.answer("Вы вернулись к выбору темы.", reply_markup=make_paginated_keyboard(topics, "topic", 0))
    else:
        await callback.message.answer("Темы не найдены. Вернитесь к выбору адреса.")
        await cancel_to_addresses(callback, state)

@user_private_router.callback_query(F.data == "cancel_to_addresses")
async def cancel_to_addresses(callback: CallbackQuery, state: FSMContext):
    user_id = get_user_id(callback.from_user.id)
    addresses = get_available_addresses(user_id)
    await state.set_state(SurveyState.choosing_address)
    await callback.message.answer("Вы вернулись к выбору адреса.", reply_markup=make_paginated_keyboard(addresses, "address", 0))

@user_private_router.message(SurveyState.answering_questions)
async def answer_questions(message: Message, state: FSMContext):
    data = await state.get_data()
    q_index = data['q_index']
    questions = data['questions']
    user_id = get_user_id(message.from_user.id)
    save_answer(user_id, questions[q_index][0], message.text)

    q_index += 1
    if q_index < len(questions):
        await state.update_data(q_index=q_index)
        await message.answer(questions[q_index][1], reply_markup=cancel_keyboard())
    else:
        await message.answer("Вы завершили тему.", reply_markup=start_keyboard())
        await state.clear()

@user_private_router.message(Command("about"))
async def about(message: Message):
    await message.answer("Бот для проверок по адресам и темам. Регистрация обязательна. Ответы сохраняются. Администратор может сбросить результаты.")

@user_private_router.message(Command("admin"))
async def admin_cmd(message: Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer("Выберите действие:\n"
                             "/export_answers - выгрузить ответы в Excel\n"
                             "/reset_answers - сбросить все ответы\n"
                             "/check_progress - проверить прогресс")
    else:
        await message.answer("Доступ запрещен.")

@user_private_router.message(Command("reset_answers"))
async def reset_answers(message: Message):
    if message.from_user.id in ADMIN_IDS:
        session.query(Answer).delete()
        session.commit()
        await message.answer("Все данные о прохождении проверок были сброшены.")
    else:
        await message.answer("У вас нет доступа к этой команде.")

@user_private_router.message(Command("export_answers"))
async def export_answers(message: Message):
    if message.from_user.id in ADMIN_IDS:
        file_bytes = export_answers_to_excel()
        document = BufferedInputFile(file_bytes, filename="answers.xlsx")
        await message.answer_document(document=document, caption="Все ответы в Excel.")
    else:
        await message.answer("У вас нет доступа к этой команде.")

@user_private_router.message(Command("check_progress"))
async def check_progress(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет доступа к этой команде.")
        return

    addresses = session.query(Address).all()
    users = session.query(User).all()
    total_users = len(users)
    report = "\U0001F4CB Прогресс по адресам и темам:\n"

    for address in addresses:
        address_complete = True
        incomplete_topics_info = ""

        for topic in address.topics:
            total_questions = len(topic.questions)
            total_answers = session.query(Answer).join(Question).filter(
                Question.topic_id == topic.id
            ).count()
            topic_complete = (total_answers >= total_questions * total_users)

            if not topic_complete:
                address_complete = False
                incomplete_topics_info += f"  ❌ Тема: {topic.name}\n"
                for question in topic.questions:
                    answered_by_users = session.query(Answer).filter(Answer.question_id == question.id).count()
                    if answered_by_users < total_users:
                        incomplete_topics_info += f"    - Вопрос: {question.question[:50]}... ({answered_by_users}/{total_users})\n"

        report += f"\n🏢 Адрес: *{address.name}*\n\n"
        if address_complete:
            report += "  ✅ Все темы и вопросы завершены.\n"
        else:
            report += incomplete_topics_info

    await message.answer(report, parse_mode="Markdown")