import json
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "8311534959:AAEuqXgWmBJ5tnWT_NL7fMmYl9tHE3weXaY"
WEB_APP_URL = "https://woodagencym10-afk.github.io/delivery/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Кнопка для ГРУП (Inline)
def group_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧮 Відкрити калькулятор", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])

# Команда для особистих повідомлень
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    if message.chat.type == 'private':
        kb = [[KeyboardButton(text="🧮 Розрахувати доставку", web_app=WebAppInfo(url=WEB_APP_URL))]]
        markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Вітаю! Використовуйте кнопку внизу:", reply_markup=markup)
    else:
        await message.answer("Натисніть кнопку для розрахунку:", reply_markup=group_keyboard())

# Команда спеціально для ГРУП
@dp.message(Command("calc"))
async def calc_cmd(message: types.Message):
    await message.answer("🧮 Калькулятор доставки:", reply_markup=group_keyboard())

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
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
