from aiogram.fsm.state import StatesGroup, State

class UserMode(StatesGroup):
    psychologist = State()   # Режим психолога
    content_maker = State()  # Режим генератора контента