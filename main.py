import logging
from aiogram import Bot, Dispatcher, executor
from handlers import start_handler, dog_cat_handlers, admin
from database.db import init_db

API_TOKEN = "7259552036:AAFqNDeiUZelsIuj-r_aVmAjgQWh832PVvs"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Handlerlarni ro'yxatga olish
start_handler.register_handlers(dp)
dog_cat_handlers.register_handlers(dp)
admin.register_admin_handlers(dp)  # Admin handlerlarini ro'yxatga olish

# Asinxron funksiyani ishlatish
async def on_startup(dp):
    await notify_admins_on_startup(dp)  # Adminlarga xabar yuborish

async def notify_admins_on_startup(dp):
    ADMINS = [973358587]  # Admin ID sini tekshiring
    for admin_id in ADMINS:
        await bot.send_message(
            admin_id,
            "Bot muvaffaqiyatli ishga tushdi ✅"
        )

if __name__ == "__main__":
    init_db()  # Ma'lumotlar bazasini initsializatsiya qilish
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
