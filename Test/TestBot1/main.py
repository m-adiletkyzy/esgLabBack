import asyncio
from aiogram import Dispatcher

from handlers import router1, bot

from shedulling import scheduler


# Настройка логирования
#logging.basicConfig(level=logging.INFO)



async def main() -> None:
    # Создаём бота и диспетчер
    dp = Dispatcher()

    dp.include_router(router1)

    # Запуск планировщика
    scheduler.start()

    # And the run events dispatching
    await dp.start_polling(bot)




if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())