from aiogram.fsm.state import State, StatesGroup

class RegisterState(StatesGroup):
    last_name = State()
    first_name = State()
    middle_name = State()

class SurveyState(StatesGroup):
    choosing_address = State()
    choosing_topic = State()
    answering_questions = State()