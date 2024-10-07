from aiogram.fsm.context import FSMContext
from ..components.db import Database
from ..components.language import Language
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from ..components.config import admin_id
from ..components.instance import bot, visual_mode_dict
from ..components.user import UserInfo
import logging
import time
# import process
import asyncio
from ..components.logger_config import logger
from ..components.memory import Form
import re 
from ..components.image import FileManager
# from file import FileMod
from ..components.chat_keyboard import Keyboard_Manager
# from tutorial import Tutorial
import json
from .keyboard_command import Keyboard_Commands
from ..components.data_process import crea_mecard, crea_wifi, wait_user_prompt
import os
import uuid
from . import process
from ..components.language import Language

class Input:
    def __init__(self):
        self.keyboard_instance = Keyboard_Manager()
        self.keboard_command = Keyboard_Commands()
        self.language = Language()
        self.db = Database()
        pass

    async def text_for_qr(self, message: Message, state: FSMContext, visual_mode):
        info = UserInfo(message)
        user_id = info.user_id
        language_code = info.language
        language_text = Language()
        db = Database()
        try:
            visual_mode_dict[user_id] = visual_mode
            status = await info.get_user_member(user_id)
            if status == 'member' or status == 'creator' or not visual_mode:
                db.default_setting(user_id) ##default setting  
                await state.set_state(Form.Text_VisualQR)  
                text = language_text.send_text(language_code)
                saved_data = db.get_saved_data(user_id)
                keyboard =  self.keyboard_instance.mecard(message, saved_data)
                await message.reply(text, reply_markup=keyboard)
                # special_format = language_text.special_format_example(language_code)
                # await message.answer(special_format, parse_mode=ParseMode.MARKDOWN_V2)
            else:
                text = language_text.not_member_channel(language_code)
                await message.reply(text)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")
    
    async def set_image_qr(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        message_id = info.message_id
        user_text = info.user_data
        try:
            
            await state.clear()
            cancel = await self.keboard_command.cancel_operation(message, state)
            if not cancel:
                if message.web_app_data:
                    data = json.loads(message.web_app_data.data)
                    if 'password' in data:
                        user_text = crea_wifi(data)
                    else:
                        user_text = crea_mecard(data)
                else:
                    save_keyboard = self.keyboard_instance.save_message_keyboard(message)
                    await message.send_copy(user_id, reply_markup=save_keyboard)
                Database().user_text(user_id, user_text)
                if visual_mode_dict[user_id] == True:                
                    language_code = message.from_user.language_code
                    lang = Language().send_image(language_code)
                    await state.set_state(Form.Image_VisualQR)
                    keyboard =  self.keyboard_instance.cancel(message)
                    await message.reply(lang, reply_markup=keyboard)
                elif visual_mode_dict[user_id] == None:
                    await wait_user_prompt(message, state)
                else:
                    await process.create_qr(message,None) #create qr
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def convert_image_url(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        result = self.db.get_user_account(user_id)
        if result:
            username = result[0]
            wif = result[1]
            
        return

    async def recive_image(self, message: Message, is_mp4=False):
        info = UserInfo(message)
        chat_id = info.chat_id
        user_id = info.user_id
        language_code = info.language
        status = await info.get_vip_member(user_id)
        try:
            if message.document or message.photo or message.animation:
                file = message.document or message.photo[-1] or message.animation
                file_info = await bot.get_file(file.file_id)
                file_path = file_info.file_path

                uid = uuid.uuid4()   # Genera un identificatore univoco                
                file_extension = file_path.split(".")[-1]# Ottieni l'estensione del file originale                
                file_name = f"{uid}.{file_extension}"  # Crea il nuovo nome del file con l'identificatore e l'estensione    
                #file_path = os.path.join(save_dir, file_name)
                directory_path = f"UserImage"
                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)

                download_path = os.path.join(directory_path, file_name)
                #file_path = self.check_file_exists(download_path) # Aggiungi questa riga

                await bot.download_file(file_path, download_path)
                max_size = 0.1
                if is_mp4: 
                    file_extension = file_path.split(".")[-1]
                    if file_extension == 'mp4':
                        file_size = os.path.getsize(download_path) / (1024 * 1024)  # Dimensione del file in MB
                        if status != 'creator' or not 'member':
                            if file_size > 0.1:  # Se la dimensione del file è superiore a 4 MB
                                os.remove(download_path)  # Elimina il file
                                max_size_text = self.language.gif_size_exceeded(language_code, max_size)
                                return max_size_text, None
                        await process.process_convert_mp4(download_path) # Converte il file in gif
                        file_name = os.path.splitext(file_name)[0] + '.gif'
                        download_path = r"UserImage/"f"{file_name}"

                return file_name, download_path
            return None
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{chat_id}:{ex}")