import random
import requests
from aiogram import types, Dispatcher
from database.db import log_activity  # Faoliyatni loglash uchun funksiyani import qilamiz

async def send_dog_image(message: types.Message):
    """It rasmi yuborish."""
    request = requests.get("https://dog.ceo/api/breeds/image/random")
    response = request.json()
    dog_image = response['message']

    # Faoliyatni loglash
    log_activity(message.from_user.id, "DOG")

    await message.answer_photo(photo=dog_image)


import aiohttp
from aiogram import types

async def send_cat_image(message: types.Message):
    """Mushuk rasmi yuborish."""
    try:
        cat_api_url = "https://api.thecatapi.com/v1/images/search"

        # Asinxron so'rov yuborish
        async with aiohttp.ClientSession() as session:
            async with session.get(cat_api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    cat_image_url = data[0]['url']  # Rasm URL manzilini olish

                    # Rasmni yuborish
                    await message.answer_photo(photo=cat_image_url)
                else:
                    await message.answer("Kechirasiz, mushuk rasmi olishda muammo yuz berdi.")

        # Faoliyatni loglash
        log_activity(message.from_user.id, "CAT")
    except Exception as e:
        await message.answer("Kechirasiz, mushuk rasmi yuborishda muammo yuz berdi.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_dog_image, lambda message: message.text == "🐶 DOG")
    dp.register_message_handler(send_cat_image, lambda message: message.text == "🐱 CAT")
