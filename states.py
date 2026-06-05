from aiogram.dispatcher.filters.state import StatesGroup, State


class State(StatesGroup):
    menu = State()
    entering_name = State()
    entering_email = State()
    entering_number = State()


    adding = State()
    
