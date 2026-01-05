import json
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "8311534959:AAEuqXgWmBJ5tnWT_NL7fMmYl9tHE3weXaY"
WEB_APP_URL = "https://woodagencym10-afk.github.io/delivery/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Кнопка для приватних повідомлень та ГРУП
def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧮 Відкрити калькулятор", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Вітаю! Натисніть кнопку нижче, щоб розрахувати доставку:",
        reply_markup=get_main_keyboard()
    )

# Цей блок ловить дані з калькулятора (працює в приваті)
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        report = (
            f"🚀 **НОВИЙ РОЗРАХУНОК**\n"
            f"━━━━━━━━━━━━━━\n"
            f"📍 Куди: {data['city']}\n"
            f"⚖️ Вага: {data['weight']} кг\n"
            f"💰 Ціна: **{data['price']}**\n"
            f"━━━━━━━━━━━━━━\n"
            f"👤 Замовив: @{message.from_user.username or message.from_user.first_name}"
        )
        await message.answer(report, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
