import json
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ПЕРЕВІР ТОКЕН ЩЕ РАЗ У BOTFATHER ПЕРЕД ВСТАВКОЮ
BOT_TOKEN = "8540043742:AAG0jad0zre2tfJxusA-DgW05KUX62l0lWc"
WEB_APP_URL = "https://woodagencym10-afk.github.io/delivery/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Універсальна кнопка
def get_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Розрахувати", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])

@dp.message(Command("start", "calc"))
async def combined_handler(message: types.Message):
    await message.answer("Натисніть кнопку для розрахунку:", reply_markup=get_kb())

@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        text = (
            f"🚀 **НОВИЙ РОЗРАХУНОК**\n"
            f"━━━━━━━━━━━━━━\n"
            f"📍 Куди: {data['city']}\n"
            f"⚖️ Вага: {data['weight']} кг\n"
            f"💰 Ціна: **{data['price']}**\n"
            f"━━━━━━━━━━━━━━\n"
            f"👤 Замовив: @{message.from_user.username or message.from_user.first_name}"
        )
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
