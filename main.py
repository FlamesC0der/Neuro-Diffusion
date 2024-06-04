import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.handlers.handlers import router
from app.database.models import async_main

from app.middlewares.antiflood import AntiFloodMiddleware
from app.asset_manager.asset_manager import check_all_assets


async def main():
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('TG_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    dp = Dispatcher()

    dp.message.middleware(AntiFloodMiddleware())

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("✨ \x1b[32mNeuro Diffusionを起動しています\x1b[0m")
    print("✨ \x1b[32mChecking assets\x1b[0m")
    check_all_assets()
    print("✨ \x1b[32mBotを起動しています...\x1b[0m")
    # logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("✨ Stopping bot...")
    except Exception as e:
        print(f"✨ Fetal Error: \n{e}")
