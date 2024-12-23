from ..components.user import UserInfo
from aiogram.types import ReplyKeyboardRemove
from aiogram import types
import os
from ..components.instance import bot, blocked_users
from ..components import config
from ..components.db import Database
from ..components.language import Language
from ..components.image import FileManager, FileMod
from ..components.qr import QR
from ..components.chat_keyboard import Keyboard_Manager

class Send_Result:
    def __init__(self):
        self.language_instance = Language()
        self.image_instance = FileManager()
        self.qr_instance = QR()
        self.keyboard_instance = Keyboard_Manager()
        self.admin_id =config.admin_id
        self.delate = FileMod()
        self.blocked_users = blocked_users
        self.db = Database()

    async def send_result(self, message, file_name, wait_message):
        try:
            info = UserInfo(message)
            user_id = info.user_id
            keyboard = self.keyboard_instance.create_start_reply_keyboard(message)
            input_file = types.FSInputFile(file_name)  # Crea un oggetto FSInputFile dal percorso del file
            await bot.send_photo(chat_id=user_id, photo=input_file, reply_markup=keyboard)
            await bot.send_message(self.admin_id, f"{user_id}: Background Removed!")
        finally:
            await bot.delete_message(user_id, wait_message.message_id)
            self.delate.delate(user_id)
            if user_id in self.blocked_users:
                del self.blocked_users[user_id]  # sblocca utente 

    async def send_waiting_message(self, message):
            info = UserInfo(message)
            language_code = info.language
            waiting, error, code_not_found = self.language_instance.get_result_language_strings(language_code)
            return await message.answer(waiting, reply_markup=ReplyKeyboardRemove()) 

    async def send_url_message(self, url, message):
        keyboard = self.keyboard_instance.create_url_app(url, message)
        await message.reply(f"{url}", reply_markup=keyboard)
        
    async def process_results(self, results, message, file_name):
            sent_message = False
            for result in results:
                if result:
                    sent_message = True
                    if isinstance(result, dict):
                        await self.process_dictionary_result(result, message)
                    else:
                        await self.process_non_dictionary_result(result, message)                    
                    file, original_file, _, file_jpg = self.image_instance.get_file_details(file_name)
                    self.image_instance.remove_file_if_exists(file, original_file, file_jpg)
            return sent_message
        
    async def process_dictionary_result(self, result, message):
        # Elabora i risultati di tipo dizionario
        for key in result:
            urls = result[key]
            for url in urls:
                if url.startswith('http'):
                    await self.send_url_message(url, message)
                else:
                    await message.reply(url)

    async def process_non_dictionary_result(self, result, message):
        # Elabora i risultati non di tipo dizionario
        value = result.split(": ")[2]
        if value.startswith('http'):
            await self.send_url_message(value, message)
        else:
            await message.reply(result)
            
    async def send_qr_result(self, message, img_path):
            info = UserInfo(message)    
            user_id = info.user_id
            chat_id = info.chat_id
            message_id = info.message_id
            result = await self.qr_instance.readqr(img_path, user_id)
            qr = self.qr_instance.check_qr_result(result)
            Database().qr_table(user_id, qr)
            keyboard = self.keyboard_instance.custom(message, qr)   
            await self.send_image_or_gif(user_id, img_path, keyboard)
            self.delate.cleanup(img_path)
            if user_id in self.blocked_users:
                del self.blocked_users[user_id]  # sblocca utente 

    async def send_image_or_gif(self, user_id, img_path, keyboard):
            name ,estensione = os.path.splitext(img_path)
            input_file = types.FSInputFile(img_path)  # Crea un oggetto FSInputFile dal percorso del file
            ads = self.db.get_ads()
            if estensione != '.gif':
                await bot.send_photo(chat_id=user_id, caption=ads ,photo=input_file)  
            else:
                await bot.send_animation(chat_id=user_id, caption=ads ,animation=input_file)     