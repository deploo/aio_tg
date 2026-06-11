import asyncio

from aiogram import Bot, Dispatcher
from handlers import command
iport Llamam




async def main():
    bot = Bot(token="8561740580:AAEOQXMBh2PAruhUCxfx9hP0gr-583PUGY4")
    dp = Dispatcher()

    dp.include_router(command.router)



    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())