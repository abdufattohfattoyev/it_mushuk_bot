import logging
import random

import aiohttp
import requests
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.exceptions import ChatAdminRequired
from data.config import ADMINS
from loader import dp, user_db, bot
from keyboards.default.valyuta_kurs import start_knopka
from keyboards.inline.inline_knopka import menu

# Majburiy kanal ro'yxati
REQUIRED_CHANNELS = ["@Kripto_Valyutalar_Rasmiy", "@yosh_dasturcii"]

# Foydalanuvchilarning obuna bo'lganligini tekshirish uchun flag
user_subscription_status = {}

async def check_subscription(user_id):
    """
    Foydalanuvchining majburiy kanallarga obuna bo'lganligini tekshiradi.
    """
    status_dict = {}
    for channel in REQUIRED_CHANNELS:
        try:
            status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            status_dict[channel] = status.status in ["member", "administrator", "creator"]
        except ChatAdminRequired:
            status_dict[channel] = False
        except Exception as e:
            status_dict[channel] = False
            logging.error(f"Kanalni tekshirishda xatolik yuz berdi: {e}")
    return status_dict


async def ensure_subscription(message: types.Message):
    """
    Foydalanuvchining obunaga bo'lishi kerakligini tekshiradi va inline tugmalarni tayyorlaydi.
    """
    subscription_status = await check_subscription(message.from_user.id)

    # Inline tugmalarni tayyorlash
    markup = types.InlineKeyboardMarkup(row_width=1)
    all_subscribed = True
    unsubscribed_channels = []

    # Har bir kanalni tekshirish va tugmalarni yaratish
    for index, channel in enumerate(REQUIRED_CHANNELS, 1):
        is_subscribed = subscription_status.get(channel, False)
        button_text = f"{'✅' if is_subscribed else '❌'} Kanal {index}"  # Kanal nomi "Kanal 1", "Kanal 2" tarzida
        button_url = f"https://t.me/{channel.lstrip('@')}"
        markup.add(types.InlineKeyboardButton(button_text, url=button_url))

        # Agar biron bir kanalga obuna bo'lmagan bo'lsa
        if not is_subscribed:
            unsubscribed_channels.append(channel)
            all_subscribed = False

    # Obunani tekshirish tugmasi
    markup.add(types.InlineKeyboardButton("Obunani tekshirish", callback_data="check_subscription"))

    # Agar barcha kanallarga obuna bo'lsa, foydalanuvchiga ruxsat berish
    if all_subscribed:
        # Foydalanuvchi faqat bir marta xabarni oladi
        if message.from_user.id not in user_subscription_status or not user_subscription_status[message.from_user.id]:
            # Foydalanuvchiga botdan foydalanish uchun ruxsat berish
            user_subscription_status[message.from_user.id] = True
        return True, markup, unsubscribed_channels

    else:
        # Agar foydalanuvchi hali ham obuna bo'lmagan kanallar mavjud bo'lsa
        await message.answer(
            "<b>❌ Kechirasiz botimizdan foydalanishdan oldin ushbu kanallarga a'zo bo'lishingiz kerak.</b>",
            parse_mode="HTML", reply_markup=markup
        )
        return False, markup, unsubscribed_channels




@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    """
    Botning boshlang'ich komandasini ishlatadi, foydalanuvchi obunani tekshiradi.
    """
    is_subscribed, markup, _ = await ensure_subscription(message)
    if not is_subscribed:
        return

    try:
        telegram_id = message.from_user.id
        username = message.from_user.username

        if not user_db.select_user(telegram_id=telegram_id):
            user_db.add_user(telegram_id=telegram_id, username=username)

            # Foydalanuvchini sanaymiz
            count = user_db.count_users()
            text = (
                f"<b>Yangi foydalanuvchi qo'shildi:</b> {username} (<code>{telegram_id}</code>)\n"
                f"<b>Jami foydalanuvchilar soni:</b> {count}"
            )
            try:
                await bot.send_message(ADMINS[0], text, parse_mode="HTML")
            except Exception as e:
                logging.error(f"Adminlarga xabar yuborishda xatolik: {e}")


    except Exception as err:
        logging.error(f"Xatolik yuz berdi: {err}")

    await message.answer(
        f"Assalomu alaykum, It va Mushuk Rasmlari botiga xush kelibsiz {message.from_user.full_name}! 😄",
        reply_markup=start_knopka
    )


async def get_random_dog_image():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("message")
                else:
                    return None
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        return None


async def get_random_cat_image():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search") as response:
                if response.status == 200:
                    data = await response.json()
                    return data[0].get("url")
                else:
                    return None
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        return None

@dp.message_handler(text="DOG")
async def DOG(message: types.Message):
    """
    It rasmi yuboradi.
    """
    is_subscribed, markup, _ = await ensure_subscription(message)
    if not is_subscribed:
        return

    dog_image_url = await get_random_dog_image()
    if dog_image_url:
        caption = random.choice([
            "Mana sizga ajoyib it rasmi! 🐕",
            "Bu it sizga yoqadi degan umiddaman! 🐶",
            "Mana siz uchun quvnoq it rasmi! 🐩"
        ])
        await message.answer_photo(photo=dog_image_url, caption=caption)
    else:
        await message.answer("Uzr, hozircha it rasmini olib bo'lmadi. Keyinroq urinib ko'ring.")


@dp.message_handler(text="CAT")
async def CAT(message: types.Message):
    """
    Mushuk rasmi yuboradi.
    """
    is_subscribed, markup, _ = await ensure_subscription(message)
    if not is_subscribed:
        return

    cat_image_url = await get_random_cat_image()
    if cat_image_url:
        caption = random.choice([
            "Mana sizga shirin mushuk rasmi! 🐈",
            "Mushuklarni sevuvchilar uchun maxsus! 😺",
            "Mana bir ajoyib mushuk rasmi! 🐾"
        ])
        await message.answer_photo(photo=cat_image_url, caption=caption)
    else:
        await message.answer("Uzr, hozircha mushuk rasmini olib bo'lmadi. Keyinroq urinib ko'ring.")



@dp.message_handler()
async def handle_all_messages(message: types.Message):
    """
    Barcha xabarlarni qabul qilib, foydalanuvchiga botdan foydalanish imkonini beradi.
    """
    # Foydalanuvchining obunasi tekshiriladi
    is_subscribed, markup, _ = await ensure_subscription(message)

    if not is_subscribed:
        return  # Agar obuna bo'lmagan bo'lsa, xabar yubormaymiz

    # Foydalanuvchining xabarini tekshirib, unga moslashuvchan javob beramiz
    user_id = message.from_user.id

    # Agar foydalanuvchi hali bot bilan ishlashni boshlamagan bo'lsa
    if user_id not in user_subscription_status or not user_subscription_status[user_id]:
        # Yangi foydalanuvchiga botning imkoniyatlarini tushuntiruvchi xabar
        await message.answer(
            f"Assalomu alaykum, {message.from_user.first_name}! Botdan foydalanish uchun 'DOG' yoki 'CAT' tugmalarini bosing.\n"
            "Ushbu tugmalar yordamida siz ajoyib it va mushuk rasmlarini ko'rishingiz mumkin! 🐕🐈",
            reply_markup=start_knopka
        )
        # Foydalanuvchining holatini 'tayyor' qilib belgilaymiz
        user_subscription_status[user_id] = True
    else:
        # Agar foydalanuvchi botdan foydalanishni boshlagan bo'lsa
        await message.answer(
            f"Salom, {message.from_user.first_name}! Xabar qabul qilindi. Botdan bemalol foydalanishingiz mumkin.\n"
            "Agar yangi rasm ko'rmoqchi bo'lsangiz, 'DOG' yoki 'CAT' tugmalarini bosing! 🐕🐈"
        )


@dp.callback_query_handler(lambda c: c.data == "check_subscription")
async def check_subscription_callback(query: types.CallbackQuery):
    """
    Obunani tekshirish tugmasi bosilganda, foydalanuvchiga to'liq obuna bo'lishini so'raydi.
    """
    user_id = query.from_user.id
    subscription_status = await check_subscription(user_id)

    # Inline tugmalarni tayyorlash
    markup = types.InlineKeyboardMarkup(row_width=1)
    all_subscribed = True
    unsubscribed_channels = []

    # Faqat obuna bo'lmagan kanallarni tekshirish va tugmalarni yaratish
    for idx, channel in enumerate(REQUIRED_CHANNELS, 1):
        is_subscribed = subscription_status.get(channel, False)
        if not is_subscribed:
            unsubscribed_channels.append(channel)
            button_text = f"❌ Kanal {idx}"
            button_url = f"https://t.me/{channel.lstrip('@')}"
            markup.add(types.InlineKeyboardButton(button_text, url=button_url))
            all_subscribed = False

    # Obunani tekshirish tugmasi
    markup.add(types.InlineKeyboardButton("Obunani tekshirish", callback_data="check_subscription"))

    # Agar barcha kanallarga obuna bo'lsa
    if all_subscribed:
        await query.message.delete()  # Eski xabarni o'chirish
        await bot.send_message(
            user_id,
            "To'liq kanallarga a'zo bo'ldingiz! Endi botdan foydalanish uchun /start buyruqni bosing."
        )
    else:
        new_text = (
            "Siz hali barcha kanallarga obuna bo'lmagansiz. Iltimos, quyidagi kanallarga obuna bo'ling:"
        )
        if query.message.text != new_text:
            await query.message.edit_text(new_text, reply_markup=markup)

    await query.answer()

