from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from ..components.user import UserInfo
from ..components.config import admin_id
from ..components.instance import bot, visual_mode_dict
from ..components.logger_config import logger
from ..components.language import Language
from aiogram.fsm.context import FSMContext
from ..components.db import Database
from ..components.chat_keyboard import Keyboard_Manager
from ..components.image import FileMod
from .tutorial import Tutorial

class Keyboard_Commands:
    def __init__(self):
        self.db = Database()
        self.language = Language()
        self.keyboard = Keyboard_Manager()
        self.file = FileMod()
        self.tutorial = Tutorial()
        pass

    async def cancel_operation(self, callback_query: CallbackQuery):
            info = UserInfo(callback_query)
            user_id = info.user_id
            language_code = info.language
            try:
                cancel_text = self.language.operation_deleted(language_code)
                await callback_query.message.edit_text(cancel_text) # type: ignore
            except Exception as ex:
                logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
                await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def handle_back_command(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        try:
            qr = Database().get_qr(user_id)
            color = Database().get_color_from_data(user_id)
            keyboard = self.keyboard.custom(message, qr)
            await message.answer("🔙", reply_markup=keyboard)
            await state.clear()
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def handle_previous_color_command(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        color = Database().get_color_from_data(user_id)
        image = Database().get_image(user_id)
        await state.clear()
        
        #await process.process_bg_background(image, color) #da vedere perchè fa sempre None

    async def handle_ai_remover_command(self, message: Message, state: FSMContext, remover):
        info = UserInfo(message)
        user_id = info.user_id
        try:
            Database().AI_Remover(user_id, remover)
            color = Database().get_color_from_data(user_id)
            text = "AI BackgroundRemover ON ✅" if remover else "AI BackgroundRemover OFF 🚫"
            keyboard = self.keyboard.create_color_reply_keyboard(message, color, remover)
            await message.answer(text, reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def handle_confirm_command(self, message: Message):
        info = UserInfo(message)
        user_id = info.user_id
        db = Database()
        try:
            language_code = info.language    
            keyboard = self.keyboard.create_start_reply_keyboard(message)
            self.file.delate(user_id) #delate all
            qr = db.get_qr(user_id)
            confirmed = self.language.confirmed(language_code, qr)
            await message.answer(confirmed, reply_markup=keyboard)     
            await bot.send_message(admin_id, f"{user_id}: Confirmed")
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")
    
    async def background_command(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        text = info.user_data
        language_code = info.language
        user_id = info.user_id
        db = Database()
        try:
            qr = db.get_qr(message.from_user.id)
            cancel = await self.cancel_operation(message, state)

            confirm, back_text, previous_color_text, ai_remover_on_text, ai_remover_off_text = self.language.get_custom_language_strings(language_code, qr)

            if not cancel:
                if text == back_text:
                    await self.handle_back_command(message, state)
                elif text == previous_color_text:
                    await self.handle_previous_color_command(message, state)
                elif text == ai_remover_on_text:
                    await self.handle_ai_remover_command(message, state, remover=False)
                elif text == ai_remover_off_text:
                    await self.handle_ai_remover_command(message, state, remover=True)
                elif text == confirm:
                    await self.handle_confirm_command(message)
            else: 
                return 
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")
        
    async def foreground_command(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        text = info.user_data
        language_code = info.language
        cancel = await self.cancel_operation(message, state)
        user_id = info.user_id
        db = Database()
        try:
            qr = db.get_qr(message.from_user.id)
            confirm, back_text, previous_color_text, ai_remover_on_text, ai_remover_off_text = self.language.get_custom_language_strings(language_code, qr)

            if not cancel:
                if text == back_text:
                    await self.handle_back_command(message, state)
                elif text == previous_color_text:
                    await self.handle_previous_color_command(message, state)
                elif text == confirm:
                    await self.handle_confirm_command(message)
            else:
                return
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")
            
    async def cancel_operation(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        text = message.text
        language_code = info.language
        try:
            cancel = Language().cancel(language_code)
            operation_deleted = Language().operation_deleted(language_code)
            if text == cancel:           
                # active = False
                # self.user_instance.user_state(user_id, active)  
                
                await state.clear()
                keyboard = self.keyboard.create_start_reply_keyboard(message)
                await message.answer(operation_deleted, reply_markup=keyboard) 
                
                self.file.delate(user_id) #delate all

                # if user_id in blocked_users:
                #     del blocked_users[user_id]  # sblocca utente
                return True
            else :
                return False
            return
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")   
    
    async def inline_cancel_command(self, callback_query: CallbackQuery):
        info = UserInfo(callback_query)
        chat_id = info.chat_id
        message_id = info.message_id
        user_id = info.user_id
        try:            
            await bot.edit_message_text(message_id=message_id,chat_id=chat_id, text="Chiuso")
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def choose_language(self, message: Message):
        info = UserInfo(message)
        language_code = info.language
        user_id = info.user_id
        try:
            choose_lang = self.language.choose_language(language_code)
            keyboard = self.keyboard.language_setting()
            await message.reply(text=choose_lang, reply_markup=keyboard)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def language_settend(self, callback_query: CallbackQuery):
        info = UserInfo(callback_query)
        db = Database()
        user_id = info.user_id
        message_id = info.message_id
        data = info.user_data
        try:
            language_code = data.split(':')[1].strip()
            db.insert_language(user_id, language_code)
            language_choosed = self.language.language_setted(language_code)
            keyboard = self.keyboard.create_start_reply_keyboard(callback_query)
            await callback_query.message.edit_text(language_choosed)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")
        
    async def message_saved(self, callback_query: CallbackQuery):
        info = UserInfo(callback_query)
        db = Database()
        language_code = info.language
        user_id = info.user_id
        caption_text = callback_query.message.md_text
        try:
            text_saved = self.language.text_saved(language_code)
            db.saved_data(user_id, caption_text)
            await callback_query.answer(text_saved)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def choose_customization(self, message: Message):
        info = UserInfo(message)
        user_id = info.user_id
        language_code = info.language
        db = Database()
        status = await info.get_vip_member(user_id)
        tutorial_link = '<a href="https://segno.readthedocs.io/en/latest/colorful-qrcodes.html">tutorial</a>' 
        try:
            if status == 'member' or status == 'creator':
                select_personalization = self.language.select_to_customize(language_code)
                foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version = db.get_settings(user_id)
                keyboard = self.keyboard.advanced_setting(alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light)
                await message.answer(tutorial_link, reply_markup=ReplyKeyboardRemove())
                await message.reply(select_personalization, reply_markup=keyboard)
            else:
                keyboard = self.keyboard.premium_keyboard(message)
                not_vip_member = self.language.buy_premium_pack(language_code)
                await message.reply(not_vip_member, reply_markup=keyboard)
        except Exception as ex:            
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def advanced_custom(self, callback_query: CallbackQuery, state: FSMContext):
        info = UserInfo(callback_query)
        data = info.user_data
        custom = data.split(":")[1].replace("✅", "").replace("🚫", "").strip()
        
        if custom == "alignment_dark":
            await self.tutorial.tutorial_alignment_dark(callback_query, state)
        elif custom == "alignment_light":
            await self.tutorial.tutorial_alignment_light(callback_query, state)
        elif custom == "data_dark":
            await self.tutorial.tutorial_data_dark(callback_query, state)
        elif custom == "data_light":
            await self.tutorial.tutorial_data_light(callback_query, state)
        elif custom == "finder_dark":
            await self.tutorial.tutorial_finder_dark(callback_query, state)
        elif custom == "finder_light":
            await self.tutorial.tutorial_finder_light(callback_query, state)
        elif custom == "format_dark":
            await self.tutorial.tutorial_format_dark(callback_query, state)
        elif custom == "format_light":
            await self.tutorial.tutorial_format_light(callback_query, state)
        elif custom == "quiet_zone":
            await self.tutorial.tutorial_quiet_zone(callback_query, state)
        elif custom == "separator":
            await self.tutorial.tutorial_separator(callback_query, state)
        elif custom == "timing_dark":
            await self.tutorial.tutorial_timing_dark(callback_query, state)
        elif custom == "timing_light":
            await self.tutorial.tutorial_timing_light(callback_query, state)
        else:
            await callback_query.answer("Error")    