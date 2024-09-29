from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from ..components.memory import Form
from ..components.user import UserInfo
from ..components.language import Language
from ..components.db import Database
from ..components import instance
import os
import logging
from ..components import config
from ..components.chat_keyboard import Keyboard_Manager
from ..components.image import FileManager, FileMod
from .result import Send_Result
from ..components.qr import QR
from .user_input import Input

class Reader(object):
    def __init__(self):
        self.bot= instance.bot
        self.admin_id = config.admin_id
        self.blocked_users = instance.blocked_users
        self.keyboard_instance = Keyboard_Manager()
        self.image_instance = FileManager()
        self.result = Send_Result()
        self.qr_instance = QR()
        self.delate = FileMod()
        self.language_instance = Language()
        self.input_user = Input()
    pass

    async def read_process(self, message: Message, state:FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        language_code = info.language
        try:
            if user_id in self.blocked_users:
                await self.bot.send_message(instance.admin_id, f"{user_id}: Blocked")
                wait_operation = self.language_instance.wait_operation(language_code)
                await message.reply(wait_operation)
                return
            self.delate.delate(user_id)
            keyboard = self.keyboard_instance.create_start_reply_keyboard(message)
            _, file_name = await self.input_user.recive_image(message, False)
            error = await self.image_instance.check_image(file_name, message, keyboard)
            if error:
                if os.path.exists(file_name):
                    os.remove(file_name)
                return
            result = await self.read_file(message, file_name)
            if result == False:
                await self.color_choose(message, state)
            return
        except Exception as ex:
            logging.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{user_id}:{ex}")
            
    async def color_choose(self, message, state):
        keyboard = self.keyboard_instance.color_chooser(message)
        info = UserInfo(message)
        user_id = info.user_id
        await state.set_state(Form.set_bg_color)
        language_code = message.from_user.language_code
        rembg_mode = self.language_instance.rembg_mode(language_code)
        await message.answer(rembg_mode, reply_markup=keyboard)

    async def read_file(self, message, file_name):        
        wait_message = await self.result.send_waiting_message(message)
        info = UserInfo(message)
        chat_id = info.chat_id
        language_code = info.language
        waiting, error, code_not_found = self.language_instance.get_result_language_strings(language_code)            
            
        keyboard = self.keyboard_instance.create_start_reply_keyboard(message)
            
        results = await self.qr_instance.readqr(file_name, chat_id)
        sent_message = await self.result.process_results(results, message, file_name)

        if not sent_message:
            file, original_file, _, file_jpg = self.image_instance.get_file_details(file_name)
            await self.handle_not_found_message(message, code_not_found, original_file)
        await self.cleanup_after_processing(wait_message, file_name)

        # finally:
        #     await self.cleanup_after_processing(wait_message, file_name)

        return sent_message          

    async def handle_not_found_message(self, message, code_not_found, file_name):
        user_id = UserInfo(message).user_id
        await message.reply(code_not_found)
        Database().save_image(user_id, file_name)

    async def handle_exception(self, message, error, ex):
        # Gestisci le eccezioni
        user_id = user_id = message.from_user.id
        logging.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
        await message.reply(error)
        await self.bot.send_message(self.admin_id, f"{user_id}:{ex}")

    async def cleanup_after_processing(self, wait_message, file_name):
        # Esegui le operazioni di pulizia dopo l'elaborazione
        await self.bot.delete_message(wait_message.chat.id, wait_message.message_id)
        file, original_file, extention, file_jpg = self.image_instance.get_file_details(file_name)
        if extention == 'gif':
            self.image_instance.remove_file_if_exists(file, original_file, file_jpg)   
            
    def cleanup(self, img_path):
        name ,estensione = os.path.splitext(img_path)
        percorso = os.path.dirname(os.path.abspath(img_path))
        file_path = f'{percorso}\{img_path}'
        self.image_instance.remove_file_if_exists(name, img_path, file_path) #elimina file


