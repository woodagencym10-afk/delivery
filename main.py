import json
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ОБОВ'ЯЗКОВО ВСТАВТЕ НОВИЙ ТОКЕН ПІСЛЯ /REVOKE
BOT_TOKEN = "8540043742:AAHF2dJuJLAq16qM11-gmKfBqsEjeC70imo"
WEB_APP_URL = "https://woodagencym10-afk.github.io/delivery/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Кнопка, яка працює і в групах
def get_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧮 Розрахувати доставку", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])

@dp.message(Command("start", "calc"))
async def start_handler(message: types.Message):
    await message.answer("Натисніть кнопку нижче для запуску калькулятора:", reply_markup=get_keyboard())

# Цей блок працює, коли кнопка натиснута в особистих повідомленнях
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    text = f"🚀 **НОВИЙ РОЗРАХУНОК**\n📍 Місто: {data['city']}\n💰 Ціна: {data['price']}\n👤 Від: @{message.from_user.username or 'Користувач'}"
    await message.answer(text, parse_mode="Markdown")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
