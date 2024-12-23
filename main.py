from telegram_bot import QR_BOT
from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession

import asyncio
from aiogram import Bot
from commads.components.logger_config import logger
from commads.components.db import Database
from commads.components.instance import bot

async def on_start():
    #Database().copy_data()
    await bot.delete_webhook()
    Database().create_table()
    print("Bot avviato")

async def on_stop():
    Database().close_connection()
    print("Bot fermato")

async def main():
    try:       
        my_bot = QR_BOT()
        await on_start()
        await my_bot.dp.start_polling(my_bot.bot)
    except Exception as ex:
        logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
    except KeyboardInterrupt:
        print("Interrotto dall'utente")
    finally:
        # await my_bot.dp.stop_polling()
        await on_stop()
        
if __name__ == '__main__':   
    asyncio.run(main())