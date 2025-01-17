from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


start_knopka=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="DOG"),
            KeyboardButton(text="CAT"),
        ],
    ],
    resize_keyboard=True,

)


