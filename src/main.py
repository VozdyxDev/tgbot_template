import asyncio
import logging

from .bot import Bot
from .dispatcher import Dispatcher


from .filters.role import RoleFilter, AdminFilter
from .handlers.admin import register_admin
from .handlers.user import register_user

logger = logging.getLogger(__name__)


async def run():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    bot = Bot()

    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)
    register_user(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


def main():
    """Wrapper for command line"""
    try:
        asyncio.run(run())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")


if __name__ == '__main__':
    main()
