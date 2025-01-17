from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="USD🇺🇸", callback_data='usd'),
            InlineKeyboardButton(text="RUB🇷🇺", callback_data='rub'),
        ],
        [
            InlineKeyboardButton(text="EUR🇪🇺", callback_data='eur'),
            InlineKeyboardButton(text="GBP🇬🇧", callback_data='gbp'),
        ],
    ],
)


# menu_courses = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="📚 Backend", callback_data='backend'),
#             InlineKeyboardButton(text="📖 Frontend", callback_data='frontend'),
#         ],
#         [
#             InlineKeyboardButton(text="🎥 SMM", callback_data="smm"),
#             InlineKeyboardButton(text="💻 Kompyuter Savodxonligi", callback_data="cs"),
#         ],
#         [
#             InlineKeyboardButton(text="🌐 Grafik Dizayner", callback_data="grafik_dizayner"),
#             InlineKeyboardButton(text="🤖 Robototexnika", callback_data="robot"),
#         ],
#         [
#             InlineKeyboardButton(text="🔙 Ortga", callback_data="back"),
#         ],
#     ],
# )
#
# ha_yoq = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="HA", callback_data='yes'),
#             InlineKeyboardButton(text="YO'Q", callback_data='not'),
#         ],
#     ],
# )
