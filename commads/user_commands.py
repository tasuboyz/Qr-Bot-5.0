from aiogram.fsm.context import FSMContext
from .components.db import Database
from .components.language import Language
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from .components.config import admin_id
from .components.instance import bot, blocked_users
from .components.user import UserInfo
import logging
import time
# import process
import asyncio
from .components.logger_config import logger
from .components.memory import Form
import re 
from .components.image import FileManager, FileMod
# from file import FileMod
from .components.chat_keyboard import Keyboard_Manager
# from tutorial import Tutorial
from .components.language import Language
from .processing.user_input import Input
from .processing.keyboard_command import Keyboard_Commands
from .processing import process
from .components.db import Database
from .components.qr import QR

class User_Commands:
    def __init__(self):
        self.qr = QR()
        self.db = Database()
        self.language = Language()
        self.image = FileManager()
        self.file = FileMod()
        self.keyboards = Keyboard_Manager()
        self.input_user = Input()
        self.keyboard_command = Keyboard_Commands()
        self.semaforo = asyncio.Semaphore(1)
        pass    

    async def command_start_handler(self, message: Message) -> None: 
        info = UserInfo(message)
        user_id = info.user_id
        first_name = info.first_name
        language_code = info.language
        username = info.username
        try:      
            introduction = self.language.start_lang(first_name, language_code)
            keyboard = self.keyboards.create_start_reply_keyboard(message)
            if user_id in blocked_users:
                wait_operation = self.language.wait_operation(language_code)
                await message.reply(wait_operation)
                return
            await message.answer(text=introduction, reply_markup=keyboard)
            Database().insert_user_data(user_id, username)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")
        finally:
            self.file.delate(user_id)

    async def help_command(self, message: Message):
        try:
            tutorial_link = '<a href="https://telegra.ph/TUTORIAL-QR-BOT-05-05">Tutorial 👇</a>' 
            await message.reply(tutorial_link)
        except Exception as ex:            
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{ex}")

    async def normal_qr(self, message: Message, state: FSMContext):
        user_id = UserInfo(message).user_id
        try:
            await self.input_user.text_for_qr(message, state, False)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")
        
    async def visual_qr(self, message: Message, state: FSMContext):
        user_id = UserInfo(message).user_id
        try:
            await self.input_user.text_for_qr(message, state, True)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def recive_image(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        chat_id = info.chat_id
        language_code = info.language #lingua dell'utente di Telegram
        try:
            await state.clear()
            waiting = self.language.waiting(language_code)
            waiting_message = await message.answer(waiting, reply_markup=ReplyKeyboardRemove()) 
            cancel = await self.keyboard_command.cancel_operation(message, state)
            if not cancel:
                Database().default_setting(user_id) ##default setting  
                ex, file_path = await self.input_user.recive_image(message, True)
                if file_path is None:
                    await bot.delete_message(chat_id, waiting_message.message_id)
                    premium_keyboards = self.keyboards.premium_keyboard(message)
                    await message.reply(ex, reply_markup=premium_keyboards)              
                    return
                keyboard = self.keyboards.create_start_reply_keyboard(message)
                await self.image.check_image(file_path, message, keyboard)
                Database().save_image(user_id, file_path)          
                async with self.semaforo:
                    await bot.delete_message(chat_id, waiting_message.message_id)
                    await process.create_qr(message,file_path) #create qr      
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def handle_circle_qr(self, message: Message):
        info = UserInfo(message)
        user_id = info.user_id
        language_code = info.language #lingua dell'utente di Telegram
        try: 
            if user_id in blocked_users:
                wait_operation = self.language.wait_operation(language_code)
                await message.reply(wait_operation)
                await bot.send_message(admin_id, f"{user_id}: Blocked")
                return
            
            text = message.text #testo inviato
            qr = Database().get_qr(user_id)
            confirm = self.language.confirm(language_code, qr)
            if text == confirm:
                return await self.keyboard_command.handle_confirm_command(message)
            visual_qr = self.language.visual_qr(language_code)
            normal_qr = self.language.normal_qr(language_code)
            back = self.language.back(language_code)
            cancel = self.language.cancel(language_code)
            excluded_keywords = [normal_qr, visual_qr, back, cancel]
            if any(keyword in text for keyword in excluded_keywords): #impedimento attivazione qr_circle da parole chiave          
                return
            async with self.semaforo:               
                img_file = await self.qr.QR_Circle(text, message)
                if img_file:
                    ads = self.db.get_ads()
                    await bot.send_photo(info.chat_id, caption=ads ,photo=img_file)               
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")                 

    async def create_advanced_qr(self, callback_query: CallbackQuery, state: FSMContext):
        info = UserInfo(callback_query)
        await state.clear()
        db = Database()
        user_id = info.user_id
        message_id = info.message_id
        try:
            await bot.delete_message(user_id, message_id)
            file_path = db.get_image(user_id)
            await process.create_qr(callback_query, file_path) #create qr   
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")