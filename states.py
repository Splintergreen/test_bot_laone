from aiogram.filters.state import State, StatesGroup


class WheatherState(StatesGroup):
    city = State()


class CurrencyState(StatesGroup):
    from_currency = State()
    to_currency = State()
    amount = State()


class PollState(StatesGroup):
    poll_theme = State()
    questions = State()
    chat_id = State()
    anon = State()
    multiple = State()
