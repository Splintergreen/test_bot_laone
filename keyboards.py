from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_keyboard():
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Посмотреть погоду',
        callback_data='weather'
    )
    button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Конвертировать валюту',
        callback_data='currency_convert'
    )
    button_3: InlineKeyboardButton = InlineKeyboardButton(
        text='Получить милую картинку',
        callback_data='pet_image'
    )
    button_4: InlineKeyboardButton = InlineKeyboardButton(
        text='Создать опрос',
        callback_data='poll_create'
    )
    keybord: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [button_1],
            [button_2],
            [button_3],
            [button_4]
        ]
    )
    return keybord


cancel_key: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
    ]
)

pet_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text='Еще одно изображение',
            callback_data='pet_image'
            )],
        [InlineKeyboardButton(text='Основное меню', callback_data='cancel')]
    ]
)
currency_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text='Конвертировать другую валюту',
            callback_data='currency_convert'
            )],
        [InlineKeyboardButton(text='Основное меню', callback_data='cancel')]
    ]
)

weather_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text='Посмотреть погоду в другом городе',
            callback_data='weather'
            )],
        [InlineKeyboardButton(text='Основное меню', callback_data='cancel')]
    ]
)

poll_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text='Создать другой опрос?',
            callback_data='poll_create'
            )],
        [InlineKeyboardButton(text='Основное меню', callback_data='cancel')]
    ]
)
