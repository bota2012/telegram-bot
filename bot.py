import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import os

TOKEN = os.getenv("BOT_TOKEN")  # Получаем токен из переменных окружения
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

questions = [
    {"q": "Сколько будет 2+2?", "options": ["3", "4", "5", "6"], "answer": "4"},
    {"q": "Сколько будет 5*3?", "options": ["15", "10", "20", "25"], "answer": "15"},
]

user_scores = {}

@dp.message_handler(commands=['start'])
async def start_quiz(message: types.Message):
    user_scores[message.from_user.id] = {"score": 0, "q_index": 0}
    await send_question(message.from_user.id)

async def send_question(user_id):
    data = user_scores[user_id]
    if data["q_index"] < len(questions):
        q = questions[data["q_index"]]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for option in q["options"]:
            keyboard.add(KeyboardButton(option))
        await bot.send_message(user_id, q["q"], reply_markup=keyboard)
    else:
        await bot.send_message(user_id, f"Тест завершён! Ваш результат: {data['score']}/{len(questions)}")

@dp.message_handler()
async def check_answer(message: types.Message):
    data = user_scores[message.from_user.id]
    q = questions[data["q_index"]]

    if message.text == q["answer"]:
        data["score"] += 1

    data["q_index"] += 1
    await send_question(message.from_user.id)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
