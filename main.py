import logging
import random
import requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = "7259552036:AAEl9GzeUbJ1EN2e8xDYjGAtaAA8x08lFtU"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Admin Telegram ID ro'yxati
ADMINS = [973358587]  # Bu yerga admin Telegram ID'larini kiriting


async def notify_admins_on_startup(dp):
    """Bot ishlashni boshlaganda adminlarga xabar yuborish."""
    for admin_id in ADMINS:
        try:
            await bot.send_message(admin_id, "Bot muvaffaqiyatli ishga tushdi ✅")
        except Exception as e:
            logging.error(f"Admin {admin_id} ga xabar yuborishda xatolik: {e}")


# Start komandasi uchun handler
@dp.message_handler(commands="start")
async def start_handler(message: types.Message):
    username = message.from_user.full_name
    text = (
        f"Assalomu Alaykum {username}!\n\n"
        f"Itlar rasmlari va mushuklar faktlari telegram botiga xush kelibsiz!\n"
        f"Quyidagi tugmalardan birini tanlang:"
    )

    # Reply Keyboard yaratish
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    dog_button = KeyboardButton("🐶 DOG")
    cat_button = KeyboardButton("🐱 CAT")
    keyboard.add(dog_button, cat_button)

    await message.answer(text, reply_markup=keyboard)


# DOG tugmasi bosilganda rasm yuborish
@dp.message_handler(lambda message: message.text == "🐶 DOG")
async def send_dog_image(message: types.Message):
    request = requests.get("https://dog.ceo/api/breeds/image/random")
    response = request.json()
    dog_image = response['message']

    await message.answer_photo(photo=dog_image)


# CAT tugmasi bosilganda rasm yuborish
@dp.message_handler(lambda message: message.text == "🐱 CAT")
async def send_cat_image(message: types.Message):
    try:
        # Random mushuk rasmi URL
        random_param = random.randint(1, 100000)  # Har safar yangi rasm uchun tasodifiy raqam
        cat_image_url = f"https://cataas.com/cat?t={random_param}"

        # Telegramga mushuk rasmini yuborish
        await message.answer_photo(photo=cat_image_url)
    except Exception as e:
        # Xatolik yuz berganda foydalanuvchiga xabar berish
        await message.answer("Kechirasiz, mushuk rasmi yuborishda muammo yuz berdi. Keyinroq qayta urinib ko'ring.")
        logging.error(f"Error fetching cat image: {e}")


if __name__ == "__main__":
    # Botni ishga tushirishdan oldin adminlarga xabar yuborish
    executor.start_polling(dp, skip_updates=True, on_startup=notify_admins_on_startup)
