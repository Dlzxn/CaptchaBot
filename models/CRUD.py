from sqlalchemy.future import select

from models.models_db import User
from logs.loger_cfg import logger
from models.create_database import get_session


async def create_user(session, user_id: int | str, username: str | None, captcha: bool, is_admin: bool):
    """Асинхронное создание пользователя в БД"""
    async with session:
        async with session.begin():
            new_user = User(telegram_id=user_id, username=username, captcha=captcha, is_admin=is_admin)
            session.add(new_user)
            await session.commit()  # Асинхронный commit

        logger.info(f"Пользователь {username} добавлен в БД.")

async def get_user_by_id(session, user_id: str | int) -> User | None:
    """Асинхронный поиск пользователя по ID"""
    async with session:
        stmt = select(User).where(User.telegram_id == user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if user:
            logger.info(f'Пользователь {user.username} найден')
            return user

        logger.info(f"Пользователь с ID {user_id} не найден")
        return None