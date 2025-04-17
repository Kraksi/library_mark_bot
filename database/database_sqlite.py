from database.engine_sqlite import session
from database.models_sqlite import User, Address, Topic, Question, Answer
import pandas as pd
from io import BytesIO
from datetime import datetime

def user_exists(telegram_id):
    return session.query(User).filter_by(telegram_id=telegram_id).first()

def get_user_id(telegram_id):
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    return user.id if user else None

def get_available_addresses(user_id):
    all_addresses = session.query(Address).all()
    available_addresses = []

    for address in all_addresses:
        topics = session.query(Topic).filter_by(address_id=address.id).all()
        available_topics = [topic for topic in topics if get_unanswered_questions(topic.id, user_id)]
        if available_topics:
            available_addresses.append(address)

    return available_addresses

def get_topics_by_address(address_id, user_id):
    topics = session.query(Topic).filter(Topic.address_id == address_id).all()
    return [topic for topic in topics if get_unanswered_questions(topic.id, user_id)]

def get_questions(topic_id):
    return session.query(Question).filter_by(topic_id=topic_id).all()

def get_unanswered_questions(topic_id, user_id):
    questions = session.query(Question).filter_by(topic_id=topic_id).all()
    answered_question_ids = {a.question_id for a in session.query(Answer).filter_by(user_id=user_id).all()}
    return [q for q in questions if q.id not in answered_question_ids]

def save_answer(user_id, question_id, answer):
    session.add(Answer(user_id=user_id, question_id=question_id, answer=answer, timestamp=datetime.utcnow()))
    session.commit()

def export_answers_to_excel():
    answers = session.query(Answer).all()
    data = []

    for answer in answers:
        user = session.query(User).filter(User.id == answer.user_id).first()
        question = session.query(Question).filter(Question.id == answer.question_id).first()
        topic = session.query(Topic).filter(Topic.id == question.topic_id).first()
        address = session.query(Address).filter(Address.id == topic.address_id).first()
        data.append({
            "Фамилия": user.last_name,
            "Имя": user.first_name,
            "Отчество": user.middle_name,
            "Адрес": address.name,
            "Тема": topic.name,
            "Вопрос": question.question,
            "Ответ": answer.answer,
            "Дата и время": answer.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Ответы")
    output.seek(0)

    return output.getvalue()