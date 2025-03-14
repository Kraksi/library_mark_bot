from aiogram.fsm.state import State, StatesGroup

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