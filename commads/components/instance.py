from . import config
from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

bot_token=config.TOKEN
admin_id = config.admin_id

blocked_users = {}
visual_mode_dict = {}

if config.use_local_api:
    session = AiohttpSession(
            api=TelegramAPIServer.from_base(config.api_base_url)
    )
    bot = Bot(token=bot_token, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
else:
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))