from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models_sqllite import User, Building, Topic, Question, Result

async def get_user(session: AsyncSession, user_id: int):
    print("---------------------", user_id)
    result = await session.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

async def add_user(session: AsyncSession, user_id: int, full_name: str):
    user = User(id=user_id, full_name=full_name)
    session.add(user)
    await session.commit()

async def get_buildings_with_unfinished_topics(session: AsyncSession, user_id: int):
    query = (select(Building)
             .join(Topic)
             .join(Question)
             .outerjoin(Result, (Result.question_id == Question.id) & (Result.user_id == user_id))
             .filter(Result.id == None)
             .distinct())
    result = await session.execute(query)
    return result.scalars().all()

async def get_topics_with_unfinished_questions(session: AsyncSession, user_id: int, building_id: int):
    query = (select(Topic)
             .join(Question)
             .outerjoin(Result, (Result.question_id == Question.id) & (Result.user_id == user_id))
             .filter(Result.id == None, Topic.building_id == building_id)
             .distinct())
    result = await session.execute(query)
    return result.scalars().all()

async def get_first_unfinished_question(session: AsyncSession, user_id: int, topic_id: int):
    query = (select(Question)
             .outerjoin(Result, (Result.question_id == Question.id) & (Result.user_id == user_id))
             .filter(Result.id == None, Question.topic_id == topic_id)
             .limit(1))
    result = await session.execute(query)
    return result.scalars().first()

async def save_result(session: AsyncSession, user_id: int, building_id: int, topic_id: int, question_id: int, score: int):
    result = Result(user_id=user_id, building_id=building_id, topic_id=topic_id, question_id=question_id, score=score)
    session.add(result)
    await session.commit()
