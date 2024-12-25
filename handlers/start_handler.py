from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import add_user

ADMINS = [973358587]  # Admin ID'lari

async def start_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name

    # Foydalanuvchini bazaga qo'shish
    add_user(user_id, username, full_name)

    # Adminlarga xabar yuborish
    for admin_id in ADMINS:
        await message.bot.send_message(
            admin_id,
            f"Yangi foydalanuvchi qo'shildi:\n"
            f"ID: {user_id}\n"
            f"Ismi: {full_name}\n"
            f"Username: @{username}"
        )

    # Tugmalar
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    dog_button = KeyboardButton("🐶 DOG")
    cat_button = KeyboardButton("🐱 CAT")
    keyboard.add(dog_button, cat_button)

    await message.answer(
        f"Assalomu Alaykum {full_name}!\n"
        f"It va mushuk rasmlari botiga xush kelibsiz! Quyidagi tugmalardan foydalaning:",
        reply_markup=keyboard
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands="start")
