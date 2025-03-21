# from sqlalchemy.orm import Session
# from engine import User, Building, Topic, Question, Answer, get_db

# # Сохранение пользователя
# def save_user(user_id: int, fullname: str):
#     db: Session = next(get_db())
#     user = db.query(User).filter(User.user_id == user_id).first()
#     if not user:
#         user = User(user_id=user_id, fullname=fullname)
#         db.add(user)
#         db.commit()

# # Получение вопросов по теме
# def get_questions_by_topic(topic_id: int, user_id: int):
#     db: Session = next(get_db())
#     questions = (
#         db.query(Question)
#         .outerjoin(Answer, (Question.id == Answer.question_id) & (Answer.user_id == user_id))
#         .filter(Question.topic_id == topic_id, Answer.id.is_(None))
#         .all()
#     )
#     return [(question.id, question.text) for question in questions]

# # Сохранение ответа
# def save_answer(user_id: int, question_id: int, rating: int):
#     db: Session = next(get_db())
#     answer = Answer(user_id=user_id, question_id=question_id, rating=rating)
#     db.add(answer)
#     db.commit()

# # Получение зданий с непройденными вопросами
# def get_buildings_with_unanswered_questions(user_id: int):
#     db: Session = next(get_db())
#     buildings = (
#         db.query(Building)
#         .filter(
#             ~db.query(Topic)
#             .join(Question)
#             .outerjoin(Answer, (Question.id == Answer.question_id) & (Answer.user_id == user_id))
#             .filter(Topic.building_id == Building.id, Answer.id.is_(None))
#             .exists()
#         )
#         .all()
#     )
#     return buildings

# # Получение тем с непройденными вопросами
# def get_topics_with_unanswered_questions(user_id: int, building_id: int):
#     db: Session = next(get_db())
#     topics = (
#         db.query(Topic)
#         .filter(
#             Topic.building_id == building_id,
#             ~db.query(Question)
#             .outerjoin(Answer, (Question.id == Answer.question_id) & (Answer.user_id == user_id))
#             .filter(Question.topic_id == Topic.id, Answer.id.is_(None))
#             .exists()
#         )
#         .all()
#     )
#     return topics