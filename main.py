import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from config import BOT_TOKEN
from database.db import create_tables
from handlers.admin import register_admin_handlers
from handlers.user import register_user_handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

register_user_handlers(dp)
register_admin_handlers(dp)

if __name__ == '__main__':
    create_tables()
    executor.start_polling(dp, skip_updates=True)
