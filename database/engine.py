# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship

# # Настройки подключения к MariaDB
# DATABASE_URL = "mysql+pymysql://bot_user:tOOT00A!@192.168.9.33/bot_db"

# # Создаем движок
# engine = create_engine(DATABASE_URL, echo=True)

# # Базовый класс для моделей
# Base = declarative_base()

# # Сессия для работы с базой данных
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Модель пользователя
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, unique=True, nullable=False)
#     fullname = Column(String(255), nullable=False)

# # Модель здания
# class Building(Base):
#     __tablename__ = "buildings"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(255), unique=True, nullable=False)

# # Модель темы
# class Topic(Base):
#     __tablename__ = "topics"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(255), unique=True, nullable=False)
#     building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
#     building = relationship("Building", backref="topics")

# # Модель вопроса
# class Question(Base):
#     __tablename__ = "questions"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     text = Column(String(255), unique=True, nullable=False)
#     topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
#     topic = relationship("Topic", backref="questions")

# # Модель ответа
# class Answer(Base):
#     __tablename__ = "answers"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
#     question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
#     rating = Column(Integer, nullable=False)

# # Создание таблиц в базе данных (если их нет)
# def create_tables():
#     Base.metadata.create_all(bind=engine)

# # Получение сессии
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

