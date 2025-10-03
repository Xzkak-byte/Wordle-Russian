from aiogram.fsm.state import State,StatesGroup

class Game(StatesGroup):
    lifes = State()
    word = State()

class Edit_name(StatesGroup):
    name = State()

class AdminStates(StatesGroup):
    waiting_for_target_id = State()
    waiting_for_value = State()

class CEOState(StatesGroup):
    id = State()

class SendMessages(StatesGroup):
    msg = State()
    id = State()
    choice = State()

class WaitID(StatesGroup):
    msg = State()
    id = State()

class Mess_to_admin(StatesGroup):
    id = State()
    msg = State()   
