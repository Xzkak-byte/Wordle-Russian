import logging,os,asyncio
from aiogram import Bot,Dispatcher
from dotenv import load_dotenv
import app.handlers as handlers
import app.callbacks as callbacks
import app.admins as admin
from aiogram.fsm.storage.memory import MemoryStorage
from app.database.models import async_main
load_dotenv()
    
async def main():
    bot = Bot(token = os.getenv("TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(admin.router)
    dp.include_router(handlers.router)
    dp.include_router(callbacks.router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)

async def startup():
    await async_main()
    print("Starting bruh man...")

async def shutdown():
    print("I am leaving man, bye bye...")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Its ok bro\nI am  leaving !!!!!!!!!!!!!!!!!!!!!!")