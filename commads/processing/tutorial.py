from ..components.logger_config import logger
from ..components.user import UserInfo
from ..components.memory import Form
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from ..components.db import Database
from ..components.chat_keyboard import Keyboard_Manager
from ..components.instance import visual_mode_dict, bot
from ..components.image import FileManager
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from ..components.config import admin_id

class Tutorial:
    def __init__(self):
        self.image_instance = FileManager()
        self.keyboard_instance = Keyboard_Manager()
        self.visual_mode_dict = visual_mode_dict

    async def tutorial_common(self, message: Message, state: FSMContext, set_state, image_url, remover=None):
        info = UserInfo(message)
        chat_id = info.chat_id
        user_id = info.user_id
        try:        
            color = Database().get_color_from_data(user_id)
            keyboard = self.keyboard_instance.create_color_reply_keyboard(message, color, remover)
            await state.set_state(set_state)

            await bot.send_photo(chat_id, photo=image_url, caption="(Example 👆) Choice the color:", reply_markup=keyboard)
            # photo_message_id = photo_message.message_id
            # self.color_instance.insert_photo(chat_id, photo_message_id)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")

    async def tutorial_light(self, message: Message, state: FSMContext):
        info = UserInfo(message)
        user_id = info.user_id
        try:
            if self.visual_mode_dict[user_id] == True:  
                await self.tutorial_common(message, state, Form.set_background, "https://segno.readthedocs.io/en/latest/_images/light.png", False)
            else:
                await self.tutorial_common(message, state, Form.set_background, "https://segno.readthedocs.io/en/latest/_images/light.png")
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")
            
    async def tutorial_dark(self, message: Message, state: FSMContext):
        await self.tutorial_common(message, state, Form.set_foreground, "https://segno.readthedocs.io/en/latest/_images/dark.png")

    async def tutorial_alignment_dark(self, callback_query: CallbackQuery, state: FSMContext):
        await self.tutorial_advanced(callback_query, state, Form.set_alignment_dark, "https://segno.readthedocs.io/en/latest/_images/alignment_dark.png")

    async def tutorial_alignment_light(self, callback_query: CallbackQuery, state: FSMContext):
        await self.tutorial_advanced(callback_query, state, Form.set_alignment_light, "https://segno.readthedocs.io/en/latest/_images/alignment_light.png")

    async def tutorial_data_dark(self, callback_query: CallbackQuery, state: FSMContext):
        await self.tutorial_advanced(callback_query, state, Form.set_data_dark, "https://segno.readthedocs.io/en/latest/_images/data_dark.png")

    async def tutorial_data_light(self, callback_query: CallbackQuery, state: FSMContext):
        await self.tutorial_advanced(callback_query, state, Form.set_data_light, "https://segno.readthedocs.io/en/latest/_images/data_light.png")

    async def tutorial_finder_dark(self, callback_query: CallbackQuery, state: FSMContext):
        await self.tutorial_advanced(callback_query, state, Form.set_finder_dark, "https://segno.readthedocs.io/en/latest/_images/finder_dark.png")

    async def tutorial_finder_light(self, callback_query: CallbackQuery, state: FSMContext):
        await self.tutorial_advanced(callback_query, state, Form.set_finder_light, "https://segno.readthedocs.io/en/latest/_images/finder_light.png")

    async def tutorial_format_dark(self, callback_query: CallbackQuery, state: FSMContext):
        await self.tutorial_advanced(callback_query, state, Form.set_format_dark, "https://segno.readthedocs.io/en/latest/_images/format_dark.png")

    async def tutorial_format_light(self, callback_query: CallbackQuery, state: FSMContext):
        await self.tutorial_advanced(callback_query, state, Form.set_format_light, "https://segno.readthedocs.io/en/latest/_images/format_light.png")

    async def tutorial_quiet_zone(self, callback_query: CallbackQuery, state: FSMContext):
        await self.tutorial_advanced(callback_query, state, Form.set_quiet_zone, "https://segno.readthedocs.io/en/latest/_images/quiet_zone.png")

    async def tutorial_separator(self, callback_query: CallbackQuery, state: FSMContext):
        await self.tutorial_advanced(callback_query, state, Form.set_separator, "https://segno.readthedocs.io/en/latest/_images/separator.png")

    async def tutorial_timing_dark(self, callback_query: CallbackQuery, state: FSMContext):
        await self.tutorial_advanced(callback_query, state, Form.set_timing_dark, "https://segno.readthedocs.io/en/latest/_images/timing_dark.png")

    async def tutorial_timing_light(self, callback_query: CallbackQuery, state: FSMContext):
        await self.tutorial_advanced(callback_query, state, Form.set_timing_light, "https://segno.readthedocs.io/en/latest/_images/timing_light.png")

    async def tutorial_advanced(self, callback_query: CallbackQuery, state: FSMContext, set_state, image_url, remover=None):
        info = UserInfo(callback_query)
        chat_id = info.chat_id
        user_id = info.user_id
        message_id = info.message_id
        try:        
            color = Database().get_color_from_data(user_id)
            keyboard = self.keyboard_instance.create_color_reply_keyboard(callback_query, color, remover)
            await state.set_state(set_state)

            await callback_query.message.edit_text("(Example 👇) Choice the color:")
            await bot.send_photo(chat_id, photo=image_url, reply_markup=keyboard)
            # photo_message_id = photo_message.message_id
            # self.color_instance.insert_photo(chat_id, photo_message_id)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione: {ex}", exc_info=True)
            await bot.send_message(admin_id, f"{user_id}:{ex}")