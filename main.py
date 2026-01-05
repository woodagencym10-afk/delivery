import json
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ТОКЕН ТА ПОСИЛАННЯ (мають бути саме так, у лапках)
BOT_TOKEN = "8311534959:AAEuqXgWmBJ5tnWT_NL7fMmYl9tHE3weXaY"
WEB_APP_URL = "https://woodagencym10-afk.github.io/delivery/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧮 Відкрити калькулятор", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await message.answer("Вітаю! Натисніть кнопку нижче, щоб розрахувати вартість доставки:", reply_markup=markup)

@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        text = (
            f"🚀 **НОВИЙ РОЗРАХУНОК**\n"
            f"━━━━━━━━━━━━━━\n"
            f"📍 Місто: {data['city']}\n"
            f"⚖️ Вага: {data['weight']} кг\n"
            f"🛣️ Відстань: {data['dist']} км\n"
            f"💰 Ціна: {data['price']}\n"
            f"━━━━━━━━━━━━━━\n"
            f"👤 Менеджер: @{message.from_user.username or message.from_user.first_name}"
        )
        await message.answer(text, parse_mode="Markdown")
    except Exception:
        await message.answer("Помилка обробки даних")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
