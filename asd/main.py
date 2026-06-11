import asyncio
import Llama
from aiogram import Bot, Dispatcher
from handlers import command

# Загружаем модель
llm = Llama(
    model_path="models/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,      # контекст
    n_threads=8,     # потоки CPU
    n_gpu_layers=35  # если есть NVIDIA GPU
)



async def main():
    bot = Bot(token="8561740580:AAEOQXMBh2PAruhUCxfx9hP0gr-583PUGY4")
    dp = Dispatcher()

    dp.include_router(command.router)



    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())