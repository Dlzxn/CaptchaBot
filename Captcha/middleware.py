from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message, FSInputFile
from aiogram import Bot, BaseMiddleware
from typing import Awaitable, Dict, Any, Callable
from time import time as t
import random, os, asyncio
from dotenv import load_dotenv

from models.CRUD import get_user_by_id, create_user
from Captcha.create_captcha import generate_image_captcha, generate_math_image_captcha
from models.create_database import get_session
from logs.loger_cfg import logger

load_dotenv()

USER_CAPTCHA: dict = {}


class CaptchaMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, session_maker):
        super().__init__()
        self.bot = bot
        self.session_maker = session_maker  # Сохраняем sessionmaker
        self.time = os.getenv("TIME")

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:

        async with self.session_maker() as session:
            user_in_db = await get_user_by_id(session, event.from_user.id)

            if user_in_db is not None:
                return await handler(event, data)

            user_captcha = USER_CAPTCHA.get(str(event.from_user.id))
            if user_captcha:
                if str(user_captcha["answer"]) == str(event.text):
                    # Создаем пользователя через ту же сессию
                    await create_user(
                        session = session,
                        user_id = event.from_user.id,
                        username=event.from_user.username,
                        captcha=True,
                        is_admin=False
                    )
                    logger.info(f'Создан новый пользователь - {event.from_user.username}')
                    if os.path.exists(user_captcha[str(event.from_user.id)]["path"]):
                        os.remove(user_captcha[str(event.from_user.id)]["path"])
                    del USER_CAPTCHA[str(event.from_user.id)]
                    await event.answer("✅ Капча пройдена! Добро пожаловать.")
                    return await handler(event, data)
                else:
                    await self.bot.delete_message(message_id=event.message_id, chat_id=event.chat.id)
                    return

            else:
                await self.bot.delete_message(message_id=event.message_id, chat_id=event.chat.id)
                rand_num: int = random.randint(1, 2)
                if rand_num == 1:
                    answer, path = generate_math_image_captcha()
                else:
                    answer, path = generate_image_captcha()

                USER_CAPTCHA[str(event.from_user.id)] = {
                    "answer": answer,
                    "time_start": t(),
                }

                # Отправка капчи
                try:
                    USER_CAPTCHA[str(event.from_user.id)] = {
                        "answer": answer,
                        "time_start": t(),
                        "path": path  # Сохраняем путь!
                    }

                    photo = FSInputFile(path)
                    try:
                        await self.bot.send_photo(
                            event.from_user.id,
                            photo=photo,
                            caption="Введите ответ в чат."
                        )
                    except TelegramForbiddenError:
                        message_delete = await self.bot.send_photo(
                            event.chat.id,
                            photo=photo,
                            caption="Введите ответ в чат."
                        )
                        await asyncio.sleep(int(self.time))

                        await self.bot.delete_message(message_id=message_delete.message_id, chat_id=message_delete.chat.id)
                    except Exception as err:
                        logger.error(err)

                    # Таймер удаления
                    await asyncio.sleep(int(self.time))

                    # Проверка и удаление
                    user_id_str = str(event.from_user.id)
                    if user_id_str in USER_CAPTCHA:
                        user_captcha = USER_CAPTCHA[user_id_str]
                        logger.info(f"Пользователь {event.from_user.id} удален: капча не пройдена")

                        if "path" in user_captcha and os.path.exists(user_captcha["path"]):
                            os.remove(user_captcha["path"])

                        del USER_CAPTCHA[user_id_str]
                        await self.bot.ban_chat_member(
                            chat_id=event.chat.id,
                            user_id=event.from_user.id
                        )
                except Exception as e:
                    logger.error(f"Ошибка: {str(e)}")
