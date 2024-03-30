import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from config_data.config import Config, load_config
from handlers import user_handlers, other_handlers
from keyboards.set_menu import set_main_menu

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting Bot')

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token,
              default=DefaultBotProperties(parse_mode='HTML'))

    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await dp.start_polling(bot)

asyncio.run(main())



