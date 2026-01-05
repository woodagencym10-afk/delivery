import json
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ВСТАВ СЮДИ НОВИЙ ТОКЕН, ЯКИЙ ДАВ BOTFATHER ПІСЛЯ /REVOKE
BOT_TOKEN = "8540043742:AAHF2dJuJLAq16qM11-gmKfBqsEjeC70imo"
WEB_APP_URL = "https://woodagencym10-afk.github.io/delivery/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Найпростіша кнопка без зайвих символів
def simple_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Відкрити калькулятор", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])

# Реагує на команди та ключові слова в групі
@dp.message(F.text)
async def message_handler(message: types.Message):
    msg_text = message.text.lower()
    if any(word in msg_text for word in ["/start", "/calc", "розрахунок", "доставка"]):
        await message.answer("📊 Натисніть для розрахунку:", reply_markup=simple_kb())

@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        report = (
            f"🚀 НОВИЙ РОЗРАХУНОК\n"
            f"📍 Куди: {data['city']}\n"
            f"💰 Ціна: {data['price']}\n"
            f"👤 Замовив: @{message.from_user.username or message.from_user.first_name}"
        )
        await message.answer(report)
    except Exception as e:
        logging.error(f"Error: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
