from .components.instance import bot
from .components.config import admin_id
from .components.chat_keyboard import Keyboard_Manager
from .components.image import FileManager, FileMod
from .components.db import Database
from aiogram.types import CallbackQuery, Message, FSInputFile
from .components.user import UserInfo
from .components.logger_config import logger
from aiogram.fsm.context import FSMContext
from .components.memory import Form
from .user_commands import User_Commands

class Admin_Commands:
    def __init__(self):
        self.keyboards = Keyboard_Manager()
        self.image = FileManager()
        self.db = Database()
        self.command = User_Commands()

    async def user_commands(self, callback_query: CallbackQuery):
        info = UserInfo(callback_query)
        chat_id = info.chat_id
        user_id = info.user_id
        question = info.user_data
        message_id = info.message_id
        if user_id == admin_id:
            try:
                keyboard = self.keyboards.create_user_keyboard()
                await bot.send_message(chat_id, "Scegli l'opzione:", reply_markup=keyboard)
            except Exception as ex:
                logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
                await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def process_callback_view_users(self, callback_query: CallbackQuery):
            info = UserInfo(callback_query)
            chat_id = info.chat_id
            user_id = info.user_id
            question = info.user_data
            message_id = info.message_id
            # user_instance.Open()
            try:
                results = Database().write_ids()
                file = FileMod()
                await file.write_ids(results)
                count_users = Database().count_users()
                await bot.delete_message(chat_id, message_id)
                input_file = FSInputFile("ids.txt")
                await bot.send_document(admin_id, document=input_file, caption=f"👤 Il numero di utenti è {count_users}")
                # await bot.send_message(admin_id, f"👤 Il numero di utenti è {count_users}")  
            except Exception as ex:
                logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
                await bot.send_message(admin_id, f"{user_id}:{ex}")
            
    async def clean_inactive_users(self, callback_query: CallbackQuery):       
        count = 0
        id_to_delate = []
        try:
            counter = await callback_query.message.answer(f"{count}")
            async for user_id in self.db.users_ids():
                try:
                    await bot.send_chat_action(user_id[0], "typing")

                    #logger.error(f"{user_id[0]} Sended! {count}")
                    
                    count += 1
                except Exception as e:     
                    #logger.error(f"{e}")         
                    #logger.error(f"{user_id[0]}, delated \n{e}") 
                    count += 1
                    id_to_delate.append(user_id[0])
                if count % 100 == 0:
                    await bot.edit_message_text(chat_id=admin_id, text=f"{count}", message_id=counter.message_id)
        finally:
            for ids in id_to_delate:
                self.db.delate_ids(ids)      
            await bot.send_message(admin_id, "Completed!")
                #logger.error(f"Completed!")        

    async def wait_document(self, callback_query: CallbackQuery, state: FSMContext):
        await callback_query.message.answer("Send file txt:")
        await state.set_state(Form.set_repair)

    async def repair_user_id(self, message: Message, state: FSMContext):
        await state.clear()
        try:
            _, file_path = await self.image.recive_image(message, False)
            self.db.insert_all_users(file_path)
            await message.reply("Repair succesful!")
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{ex}")
    
    async def recive_ads(self, callback_query: CallbackQuery, state: FSMContext):
        info = UserInfo(callback_query)
        chat_id = info.chat_id
        await state.set_state(Form.set_ads)  
        await bot.send_message(admin_id, "Ads:")    

    async def send_ads(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        ads = message.text
        await state.clear()
        count = 0
        #id_da_escludere = self.estrai_id("send file.txt")
        id_to_delate = []
        try:
            counter = await message.answer("0")
            async for user_id in Database().users_ids():
                #if user_id[0] in id_da_escludere:
                #    continue
                #if count == 5111:
                #    logger.error(f"Completed!")
                #    break
                try:
                    keyboard = self.keyboards.create_start_reply_keyboard(message)
                    await message.send_copy(user_id[0])
                    #logger.error(f"{user_id[0]} Sended! {count}")
                    count += 1
                    if count % 100 == 0:
                        await bot.edit_message_text(chat_id=admin_id, text=f"{count}", message_id=counter.message_id, reply_markup=keyboard)
                except Exception as e:             
                    #logger.error(f"{user_id[0]}, delated \n{e}") 
                    id_to_delate.append(user_id[0])
        finally:
            for ids in id_to_delate:
                Database().delate_ids(ids)      
            logger.error(f"Completed!") 

    async def set_place_ads(self, callback_query: CallbackQuery, state: FSMContext):
        info = UserInfo(callback_query)
        chat_id = info.chat_id
        await state.set_state(Form.set_place_ads)  
        await bot.send_message(admin_id, "ads example: <code>a href=link ads /a</code>" )

    async def recive_place_ads(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        chat_id = info.chat_id
        ads = message.text
        await state.clear()
        try:
            self.db.insert_ads(admin_id, ads)
            await message.reply("saved!")
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{ex}")