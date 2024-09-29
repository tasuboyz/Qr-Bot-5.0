from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

import os
import uuid
import shutil
from ..components.db import Database
from ..components import instance
from ..components.logger_config import logger
import asyncio 
from ..components import config

from multiprocessing import Process, process
from qrcode.image.styledpil import StyledPilImage
from ..components.language import Language
from ..components.user import UserInfo
import qrcode

from PIL import Image, ImageColor, ImageOps ,ImageDraw, ImageFont, ImageFilter
from qrcode.image.styles.moduledrawers import (
    CircleModuleDrawer, SquareModuleDrawer
)
from ..components.user import UserInfo
from ..components.image import FileManager
from ..components.qr import QR
from .result import Send_Result

result = Send_Result()
qr = QR()
image = FileManager()
language = Language()

async def create_qr(data, file_name):
    try:
        info = UserInfo(data)
        user_id = info.user_id
        language_code = info.language
        message = info.message
        waiting = language.waiting(language_code)
        error = language.error(language_code)
        wait_message = await message.answer(waiting, reply_markup=ReplyKeyboardRemove()) 
        instance.blocked_users[user_id] = True

        await process_qr_creation(data, file_name)        
    except Exception as ex:
        await handle_exception(data, ex, file_name)
    finally:
        await instance.bot.delete_message(user_id, wait_message.message_id)

async def process_qr_creation(data, file_name):
    info = UserInfo(data)
    user_id = info.user_id
    copy_file = ''
    try:
        text = Database().get_user_text(user_id) ##get user text   
        foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version = Database().get_settings(user_id)
        if file_name == None:                
            Database().AI_Remover(user_id, None)
            copy_file = qr.write_normal_qr(text, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version)
            await result.send_qr_result(data, copy_file)
        else:               
            estensione = os.path.splitext(file_name)[1]
            copy_file = f'Copy_{uuid.uuid4()}{estensione}'
            shutil.copy2(file_name, copy_file)          
            if estensione == ".gif":
                image.resize_gif(copy_file, background_color)
            else:
                image.resize(copy_file, background_color)

            qr_process = Process(target=process_create_qr, args=(user_id, text, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version, copy_file))
            qr_process.start()
            while qr_process.is_alive():
                await asyncio.sleep(1)
            await result.send_qr_result(data, copy_file)    
    except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await instance.bot.send_message(config.admin_id, f"{user_id}:{ex}")
    finally:
        if user_id in instance.blocked_users:
            del instance.blocked_users[user_id]  # sblocca utente 

async def cleanup_operations(message, wait_message):
    user_id = message.from_user.id
    try:
        await instance.bot.delete_message(wait_message.chat.id, wait_message.message_id)
        Database().delate_remover_state(user_id)
        Database().delate_colors(user_id)
        del instance.blocked_users[user_id]
    except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await instance.bot.send_message(config.admin_id, f"{user_id}:{ex}")

async def handle_exception(message, exception, file_name):
    info = UserInfo(message)
    user_id = info.user_id
    language_code = info.language
    error_occurred = language.error_occurred(language_code)
    logger.error(f"Errore durante l'esecuzione di handle_set_state: {exception} percorso:{file_name}", exc_info=True)
    await instance.bot.send_message(config.admin_id, f"{user_id}:{exception}")
    await instance.bot.send_message(user_id, error_occurred)
    
def process_create_qr(user_id, text, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version, file_name):
    try:
        qr.write_artistic_qr(user_id, text, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version, file_name)
    except Exception as ex:
        logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
        
async def process_bg_background(file_name, color):
    background_process = Process(target=process_background_remover, args=(file_name, color))
    background_process.start()
    while background_process.is_alive():
        await asyncio.sleep(1)
        
def process_background_remover(file_name, color):
    image.background_remover(file_name, color) 
    
async def process_convert_mp4(file_name):
    convert_process = Process(target=process_convertion, args=(file_name,))
    convert_process.start()
    while convert_process.is_alive():
        await asyncio.sleep(1)
    
def process_convertion(file_name):
    image.convert_mp4(file_name)
    
async def process_circular_qr(text, message, img_byte_arr):
    background_process = Process(target=process_create_cirle_qr, args=(text, message, img_byte_arr))
    background_process.start()
    while background_process.is_alive():
        await asyncio.sleep(1)
        
def process_create_cirle_qr(text, message, img_byte_arr):
    
    return
    

    
# async def custom_light(message, color, image, wait_message):
#     info = UserInfo(message)
#     user_id = info.user_id
#     process_bg_background(image, color)                        