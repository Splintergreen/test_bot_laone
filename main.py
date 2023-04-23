import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import BaseFilter, CommandStart, Text
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv

from data import cities, currency_names
from func import convert_currency, get_pet_image, what_weather
from keyboards import (cancel_key, currency_keyboard, pet_keyboard,
                       poll_keyboard, start_keyboard, weather_keyboard)
from states import CurrencyState, PollState, WheatherState

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')

redis: Redis = Redis(host='localhost')

storage: RedisStorage = RedisStorage(redis=redis)

bot: Bot = Bot(token=TG_TOKEN)
dp: Dispatcher = Dispatcher(storage=storage)


@dp.message(CommandStart())
async def start_command(message: Message):
    '''Стартовое меню, /start'''
    text = 'Вас приветствует бот по тестовому заданию от компании LaOne'
    await message.answer(text, reply_markup=start_keyboard())


@dp.callback_query(Text(text=['cancel']))
async def cancel_call(callback_query: CallbackQuery, state: FSMContext):
    '''Сбрасывает машину состояний, при нажатии кнопки "отмена".'''
    text = 'Выберите требуемое действие:'
    await callback_query.message.answer(text, reply_markup=start_keyboard())
    await state.clear()


@dp.callback_query(Text(text=['weather']))
async def weather_call(callback_query: CallbackQuery, state: FSMContext):
    '''Получить прогноз погоды.'''
    text = 'Введите название города:'
    await callback_query.message.answer(text, reply_markup=cancel_key)
    await state.set_state(WheatherState.city)


@dp.message(
        StateFilter(WheatherState.city),
        lambda x: x.text.isalpha() and x.text.title() in cities
        )
async def get_weather(message: Message, state: FSMContext):
    '''Получаем прогноз если указаный город введен корректно'''
    await state.update_data(city=message.text)
    city = await state.get_data()
    wheather = what_weather(city)
    text = f'Погода в городе {city["city"].title()}: {wheather}'
    await state.clear()
    await message.answer(text, reply_markup=weather_keyboard)


@dp.message(StateFilter(WheatherState.city))
async def wrong_city(message: Message):
    '''Обработка ошибок ввода названия города.'''
    await message.answer(
        'Некооректный ввод, ведите название города!',
        reply_markup=cancel_key
        )


@dp.callback_query(Text(text=['currency_convert']))
async def currency_call(callback_query: CallbackQuery, state: FSMContext):
    '''Конвертация валют.'''
    text = (
        'Введите название валюты которую хотите конвертировать в '
        'трехбуквенном формате, например "USD"'
        )
    await callback_query.message.answer(text, reply_markup=cancel_key)
    await state.set_state(CurrencyState.from_currency)


@dp.message(
        StateFilter(CurrencyState.from_currency),
        lambda x: (
                    F.text.is_alpha() and len(x.text) == 3 and
                    currency_names.get(x.text.upper()) is not None
                    )
            )
async def get_from_currency(message: Message, state: FSMContext):
    '''Ввод и проверка названия введенной валюты из которой конвертировать.'''
    await state.update_data(from_currency=message.text.upper())
    text = (
        'Введите название валюты в какую хотите конвертировать в '
        'трехбуквенном формате, например "RUB"'
        )
    await message.answer(text, reply_markup=cancel_key)
    await state.set_state(CurrencyState.to_currency)


@dp.message(StateFilter(CurrencyState.from_currency))
async def wrong_from_currency(message: Message):
    '''Обработка ошибок ввода названия конвертируемой валюты.'''
    await message.answer(
        'Некооректный ввод, ведите название валюты в трехбуквенном формате!',
        reply_markup=cancel_key
        )


@dp.message(
        StateFilter(CurrencyState.to_currency),
        lambda x: (
                    F.text.is_alpha() and len(x.text) == 3
                    and currency_names.get(x.text.upper()) is not None
                )
        )
async def get_to_currency(message: Message, state: FSMContext):
    '''Ввод и проверка названия введенной валюты в которую конвертировать.'''
    await state.update_data(to_currency=message.text.upper())
    await message.answer(
        'Введите количество конвертируемой валюты:',
        reply_markup=cancel_key
        )
    await state.set_state(CurrencyState.amount)


@dp.message(StateFilter(CurrencyState.to_currency))
async def wrong_to_currency(message: Message):
    '''Обработка ошибок ввода названия валюты в которую конвертировать.'''
    await message.answer(
        'Некооректный ввод, ведите название валюты в трехбуквенном формате!',
        reply_markup=cancel_key
        )


@dp.message(
        StateFilter(CurrencyState.amount),
        lambda x: x.text.isdigit() and int(x.text) > 0
        )
async def get_currency_amount(message: Message, state: FSMContext):
    '''Проверка количества валюты и вывод результата конвертации.'''
    await state.update_data(amount=message.text)
    currency_data = await state.get_data()
    from_currency = currency_data['from_currency']
    to_currency = currency_data['to_currency']
    amount = currency_data['amount']
    result = convert_currency(from_currency, to_currency, amount)
    text = (
        f'Результат конвертации {amount} {from_currency}'
        f' в {to_currency}: {result}'
        )
    await message.answer(text, reply_markup=currency_keyboard)
    await state.clear()


@dp.message(StateFilter(CurrencyState.amount))
async def wrong_anount(message: Message):
    '''Обработка некорректного количества валюты.'''
    await message.answer('Некорректный ввод!', reply_markup=cancel_key)


@dp.callback_query(Text(text=['pet_image']))
async def call_pet_image(callback_query: CallbackQuery):
    '''Получить изображение котика.'''
    await callback_query.message.answer_photo(
        get_pet_image(),
        reply_markup=pet_keyboard
        )


@dp.callback_query(Text(text=['poll_create']))
async def poll_create_call(callback_query: CallbackQuery, state: FSMContext):
    '''Создание опроса.'''
    await callback_query.message.answer(
        'Введите тему опроса.',
        reply_markup=cancel_key
        )
    await state.set_state(PollState.poll_theme)


@dp.message(StateFilter(PollState.poll_theme))
async def poll_theme_call(message: Message, state: FSMContext):
    '''Сохранение темы опроса.'''
    await state.update_data(poll_theme=message.text)
    await message.answer(
        'Введите список вопросов через запятую.\nМинимум 2 вопроса.'
        )
    await state.set_state(PollState.questions)


@dp.message(
        StateFilter(PollState.questions),
        lambda x: len(x.text.split(',')) > 1
        )
async def poll_questions_call(message: Message, state: FSMContext):
    '''Сохранение списка вопросов. Проверка количества вопросов.'''
    questions = message.text.split(',')
    if questions[-1] == '':
        questions.pop(-1)
    await state.update_data(questions=questions)
    await message.answer(
        'Введите ID чата куда отправить опрос или "Сюда", чтоб '
        'отправить опрос сюда.',
        reply_markup=cancel_key
        )
    await state.set_state(PollState.chat_id)


@dp.message(StateFilter(PollState.questions))
async def poll_wrong_questions_call(message: Message):
    '''Обработка некорректного количества впросов.'''
    await message.answer(
        'Должно быть минимум 2 вопроса!',
        reply_markup=cancel_key
        )


class CheckChatID(BaseFilter):
    '''Проверка существования введенного чат ID.'''
    async def __call__(self, message: Message) -> bool:
        if message.text.upper() == 'СЮДА':
            return True
        try:
            await bot.get_chat(message.text)
            return True
        except Exception:
            return False


@dp.message(StateFilter(PollState.chat_id), CheckChatID())
async def poll_chat_id_call(message: Message, state: FSMContext):
    '''Проверка и сохранение Чат ID.'''
    if message.text.upper() == 'СЮДА':
        chat_id = message.chat.id
    else:
        chat_id = message.text
    await state.update_data(chat_id=chat_id)
    await message.answer(
        'Сделать опрос анонимным? "Да"/"Нет"',
        reply_markup=cancel_key
        )
    await state.set_state(PollState.anon)


@dp.message(StateFilter(PollState.chat_id))
async def poll_wrong_chat_id_call(message: Message):
    '''Обработка некорректного ввода Чат ID.'''
    await message.answer(
        'Некорректный/несущетвующий ID!\n'
        'Попробуйте еще раз или введите "Сюда".',
        reply_markup=cancel_key
        )


@dp.message(
        StateFilter(PollState.anon), lambda x: x.text.upper() in ['ДА', 'НЕТ']
        )
async def poll_anon_call(message: Message, state: FSMContext):
    '''Анонимный опрос? Проверка введенного ответа.'''
    if message.text.upper() == 'ДА':
        await state.update_data(anon=True)
    else:
        await state.update_data(anon=False)
    await message.answer(
        'Несколько вариантов ответа? "Да"/"Нет"',
        reply_markup=cancel_key
        )
    await state.set_state(PollState.multiple)


@dp.message(StateFilter(PollState.anon))
async def poll_wrong_anon_call(message: Message):
    '''Обработка неккоректного ответа на вопрос анонимности опроса.'''
    await message.answer(
        'Введите "Да" или "Нет"',
        reply_markup=cancel_key
        )


@dp.message(
        StateFilter(PollState.multiple),
        lambda x: x.text.upper() in ['ДА', 'НЕТ']
        )
async def send_poll(message: Message, state: FSMContext):
    '''Множественный выбор? Проверка введенного ответа. Отправка опроса.'''
    if message.text.upper() == 'ДА':
        await state.update_data(multiple=True)
    else:
        await state.update_data(multiple=False)
    data = await state.get_data()
    await message.answer(
        'Опрос создан и отправлен.',
        reply_markup=poll_keyboard
        )
    await bot.send_poll(
        chat_id=data['chat_id'],
        question=data['poll_theme'],
        options=data['questions'],
        is_anonymous=data['anon'],
        allows_multiple_answers=data['multiple']
        )
    await state.clear()


@dp.message(StateFilter(PollState.multiple))
async def wrong_multiple_poll(message: Message):
    '''Обработка некорректного ответа на вопрос множественного выбоора.'''
    await message.answer(
        'Введите "Да" или "Нет"',
        reply_markup=poll_keyboard
        )


@dp.message()
async def any_message(message: Message):
    '''Обработка любых сообщений не относящихся к основной логике бота.'''
    await message.answer(
        'Не понимаю Вас, введите /start для перехода в основное меню'
        )


if __name__ == '__main__':
    dp.run_polling(bot)
