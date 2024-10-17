import sqlite3
import json

from aiogram.types import ReplyKeyboardRemove, Message

from aiogram.fsm.context import FSMContext
from ..components.memory import Form
from ..components.user import UserInfo
from ..components.db import Database
import asyncio
from ..components.instance import blocked_users, bot
from . import process
from ..components.logger_config import logger
from ..components import config
from ..components.chat_keyboard import Keyboard_Manager
from ..components.language import Language
from .result import Send_Result
import re

class ColorManager: # crea una classe per gestire i colori e le impostazioni del QR
    def __init__(self):
        self.admin_id = config.admin_id
        self.keyboard_instance = Keyboard_Manager()
        self.language_instance = Language()
        self.result = Send_Result()
        self.semaforo = asyncio.Semaphore(1)

    def get_color_from_web(self, message: Message):
        info = UserInfo(message)
        user_id = info.user_id
        try:
            data = json.loads(message.web_app_data.data) ##get data responce
            color = tuple(data['rgb'].values())     
            color = ','.join(map(str, color))
            Database().save_color_in_settings(user_id, color)
            return color
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            
    async def color_choose(self, message: Message, state: FSMContext):
        keyboard = self.keyboard_instance.color_chooser(message)
        info = UserInfo(message)
        user_id = info.user_id
        try:
            await state.set_state(Form.set_color)
            language_code = info.language
            rembg_mode = self.language_instance.rembg_mode(language_code)
            await message.answer(rembg_mode, reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(self.admin_id, f"{user_id}:{ex}")
        
    async def recive_web_color(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        message_id = info.message_id 
        chat_id = info.chat_id
        try:
            await state.clear()
            blocked_users[user_id] = True
            wait_message = await self.result.send_waiting_message(message)
            await bot.delete_message(user_id, message_id)
            color = self.get_color_from_web(message)
            file_name = Database().get_image(user_id)
            async with self.semaforo:   
                await process.process_bg_background(file_name, color)
                await self.result.send_result(message, file_name, wait_message)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(self.admin_id, f"{user_id}:{ex}")

    async def handle_set_background(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id       
        try:                     
            color = self.get_color_from_web(message)
            image = Database().get_image(user_id)
            text = Database().get_user_text(user_id) ##get user text
            remover = Database().view_remover_state(user_id)    
            language_code = message.from_user.language_code    
            blocked_users[user_id] = True       
            if remover:
                waiting = self.language_instance.waiting(language_code)    #attesa
                wait_message = await message.answer(waiting, reply_markup=ReplyKeyboardRemove())
                async with self.semaforo:
                    await process.process_bg_background(image, color)   
                await bot.delete_message(wait_message.chat.id, wait_message.message_id)
            foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version = Database().get_settings(user_id)
            Database().save_settings(user_id, foreground_color, color, alignment_dark, color, data_dark, color, finder_dark, color, color, color, timing_dark, color, version_dark, color, version)        
            await process.create_qr(message, image) #create qr            
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(self.admin_id, f"{user_id}:{ex}")
        finally:
            await state.clear()            
            if user_id in blocked_users:
                del blocked_users[user_id]
            
    async def handle_set_foreground(self, message: Message, state: FSMContext):
        user_id = message.from_user.id
        await state.clear()
        try:
            color = self.get_color_from_web(message)
            image = Database().get_image(user_id)
            await self.custom_dark(message, color, image)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(self.admin_id, f"{user_id}:{ex}") 

    async def custom_light(self, message: Message, color):
        info = UserInfo(message)
        user_id = info.user_id
        foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version = Database().get_settings(user_id)
        Database().save_settings(user_id, foreground_color, color, alignment_dark, color, data_dark, color, finder_dark, color, quiet_zone, separator, timing_dark, color, version_dark, color, version)
        #await process.create_qr(message, image) #create qr
            
    async def custom_dark(self, message: Message, color):
        info = UserInfo(message)
        user_id = info.user_id
        foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version = Database().get_settings(user_id)
        Database().save_settings(user_id, color, background_color, color, alignment_light, color, data_light, color, finder_light, quiet_zone, separator, color, timing_light, color, version_light, version)
        #await process.create_qr(message, image) #create qr

    async def advanced_custom_color(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        db = Database()
        user_text = message.text
        language_code = info.language
        try:
            color = self.get_color_from_web(message)
            foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version = db.get_settings(user_id)
            current_state = await state.get_state()
            
            if current_state == Form.set_alignment_dark:
                await message.reply("alignment_dark")
                db.save_settings(user_id, foreground_color, background_color, color, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version)
            elif current_state == Form.set_alignment_light:
                await message.reply("alignment_light")
                db.save_settings(user_id, foreground_color, background_color, alignment_dark, color, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version)
            elif current_state == Form.set_data_dark:
                await message.reply("data_dark")
                db.save_settings(user_id, foreground_color, background_color, alignment_dark, alignment_light, color, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version)
            elif current_state == Form.set_data_light:
                await message.reply("data_light")
                db.save_settings(user_id, foreground_color, background_color, alignment_dark, alignment_light, data_dark, color, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version)
            elif current_state == Form.set_finder_dark:
                await message.reply("finder_dark")
                db.save_settings(user_id, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, color, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version)
            elif current_state == Form.set_finder_light:
                await message.reply("finder_light")
                db.save_settings(user_id, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, color, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version)
            elif current_state == Form.set_format_dark:
                await message.reply("format_dark")
                db.save_settings(user_id, foreground_color, background_color, alignment_dark, alignment_light, color, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version)
            elif current_state == Form.set_format_light:
                await message.reply("format_light")
                db.save_settings(user_id, foreground_color, background_color, alignment_dark, alignment_light, data_dark, color, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version)
            elif current_state == Form.set_quiet_zone:
                await message.reply("quiet_zone")
                db.save_settings(user_id, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, color, separator, timing_dark, timing_light, version_dark, version_light, version)
            elif current_state == Form.set_separator:
                await message.reply("separator")
                db.save_settings(user_id, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, color, timing_dark, timing_light, version_dark, version_light, version)
            elif current_state == Form.set_timing_dark:
                await message.reply("timing_dark")
                db.save_settings(user_id, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, color, timing_light, version_dark, version_light, version)
            elif current_state == Form.set_timing_light:
                await message.reply("timing_light")
                db.save_settings(user_id, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, color, version_dark, version_light, version)
            else:
                await message.reply("Error")
            personalize_color = self.language_instance.select_to_customize(language_code)
            foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version = db.get_settings(user_id)
            keyboard = self.keyboard_instance.advanced_setting(alignment_dark=alignment_dark, alignment_light=alignment_light, data_dark=data_dark, data_light=data_light, finder_dark=finder_dark, finder_light=finder_light, quiet_zone=quiet_zone, separator=separator, timing_dark=timing_dark, timing_light=timing_light)
            await message.reply(personalize_color, reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(self.admin_id, f"{user_id}:{ex}")

    def is_rgb(self, color):
        # Controlla se il colore è in formato RGB
        rgb_pattern = r'^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$'
        return re.match(rgb_pattern, color)

    def hex_to_rgb(self, hex_color):
        # Remove the '#' symbol
        hex_color = hex_color.lstrip('#')
        # Convert the HEX color to RGB
        rgb_values = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"{rgb_values[0]}, {rgb_values[1]}, {rgb_values[2]}"

    def process_color(self, color):
        if self.is_rgb(color):
            return color
        else:
            rgb_color = self.hex_to_rgb(color)
            return rgb_color