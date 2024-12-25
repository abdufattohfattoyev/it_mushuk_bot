from aiogram import types
from aiogram.types import ContentTypes
from database.db import get_all_users

ADMINS = [973358587]  # Adminlar ID sini bu yerga yozing


async def handle_advertisement_content(message: types.Message):
    """Admin reklama yuborish uchun komanda."""
    if message.from_user.id not in ADMINS:
        await message.reply("Sizda reklama yuborish huquqi yo'q.")
        return

    # Admin reklama yuborishni boshlaydi
    if message.text == "/reklama":
        await message.reply("Reklama matnini yoki media yuboring (video, audio, text).")
    else:
        # Foydalanuvchilarga reklama yuborish
        all_users = get_all_users()  # Faol foydalanuvchilarni olish
        for user_id in all_users:
            try:
                # Matn bo'lsa
                if message.content_type == ContentTypes.TEXT:
                    await message.bot.send_message(user_id, message.text)

                # Video bo'lsa
                elif message.content_type == ContentTypes.VIDEO:
                    await message.bot.send_video(user_id, message.video.file_id)

                # Audio bo'lsa
                elif message.content_type == ContentTypes.AUDIO:
                    await message.bot.send_audio(user_id, message.audio.file_id)

                # Rasm bo'lsa
                elif message.content_type == ContentTypes.PHOTO:
                    await message.bot.send_photo(user_id, message.photo[-1].file_id)

                # Fayl bo'lsa
                elif message.content_type == ContentTypes.DOCUMENT:
                    await message.bot.send_document(user_id, message.document.file_id)

            except Exception as e:
                print(f"Foydalanuvchiga yuborishda xato: {e}")

        await message.reply("Reklama barcha foydalanuvchilarga yuborildi.")


def register_admin_handlers(dp):
    dp.register_message_handler(handle_advertisement_content, commands="reklama", state="*")
