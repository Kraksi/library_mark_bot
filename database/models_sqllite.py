from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.engine_sqllite import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)

class Building(Base):
    __tablename__ = 'buildings'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Topic(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    building_id = Column(Integer, ForeignKey('buildings.id'))
    building = relationship('Building')

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    topic = relationship('Topic')

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')
    date = Column(DateTime, default=datetime.utcnow)
    building_id = Column(Integer, ForeignKey('buildings.id'))
    building = relationship('Building')
    topic_id = Column(Integer, ForeignKey('topics.id'))
    topic = relationship('Topic')
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship('Question')
    score = Column(Integer, nullable=False)
