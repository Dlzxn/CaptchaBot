# main.py (обновленная версия)
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
import os
import asyncio
from models.create_database import init_db, get_session  # Импорт новых функций
from Captcha.middleware import CaptchaMiddleware
from logs.loger_cfg import logger

logger.info("Запуск бота")

load_dotenv()
TOKEN = os.getenv("TOKEN")


async def main():
    # 1. Инициализация БД
    await init_db()

    # 2. Инициализация бота
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # 3. Передаем sessionmaker в middleware
    dp.message.middleware(CaptchaMiddleware(bot, get_session()))

    @dp.message()
    async def message(message: types.Message):
        logger.info("СOOБЩЕНИЕ")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())