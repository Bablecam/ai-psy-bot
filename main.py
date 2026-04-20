import asyncio
import sys
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router

# Настройка логирования (чтобы видеть только важные сообщения, а не мусор)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(router)
    
    # Удаляем вебхуки, чтобы бот не пытался обработать старые обновления
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("🤖 Бот запущен! Архитектура модульная. Жду сообщений... (Для остановки нажми Ctrl+C)")
    
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    try:
        # Запускаем, игнорируя KeyboardInterrupt (Ctrl+C)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен вручную. До свидания!")
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")