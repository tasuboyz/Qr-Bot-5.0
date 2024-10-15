from commads.components import config

from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart, Command

from commads.components.db import Database
import logging
from commads.components.language import Language
from commads.components.memory import Form
from commads.admin_command import Admin_Commands

import asyncio
from commads.components import instance
from commads.user_commands import User_Commands
from commads.processing.color import ColorManager
from commads.processing.keyboard_command import Keyboard_Commands
from commads.processing.user_input import Input
from commads.processing.tutorial import Tutorial
from commads.processing.read_qr import Reader

class QR_BOT():
    def __init__(self):
        self.bot_token = config.TOKEN
        self.admin_id = config.admin_id
        self.save_dir = r""
        self.bot = instance.bot
        self.dp = Dispatcher()
        self.db = Database()
        self.language = Language()
        self.color = ColorManager()  
        self.keyboard_commands = Keyboard_Commands()
        self.user_commands = User_Commands()
        self.admin_command = Admin_Commands()
        self.input_user = Input()
        self.tutorial = Tutorial()
        self.reader = Reader()
        
        self.semaforo = asyncio.Semaphore(1)
        self.polling_started = False

        #advanced custom
        self.dp.message(Form.set_alignment_dark, F.text.in_(self.language.back_to_custom))(self.keyboard_commands.choose_customization)
        self.dp.message(Form.set_alignment_light, F.text.in_(self.language.back_to_custom))(self.keyboard_commands.choose_customization)
        self.dp.message(Form.set_data_dark, F.text.in_(self.language.back_to_custom))(self.keyboard_commands.choose_customization)
        self.dp.message(Form.set_data_light, F.text.in_(self.language.back_to_custom))(self.keyboard_commands.choose_customization)
        self.dp.message(Form.set_finder_dark, F.text.in_(self.language.back_to_custom))(self.keyboard_commands.choose_customization)
        self.dp.message(Form.set_finder_light, F.text.in_(self.language.back_to_custom))(self.keyboard_commands.choose_customization)
        self.dp.message(Form.set_format_dark, F.text.in_(self.language.back_to_custom))(self.keyboard_commands.choose_customization)
        self.dp.message(Form.set_format_light, F.text.in_(self.language.back_to_custom))(self.keyboard_commands.choose_customization)
        self.dp.message(Form.set_quiet_zone, F.text.in_(self.language.back_to_custom))(self.keyboard_commands.choose_customization)
        self.dp.message(Form.set_separator, F.text.in_(self.language.back_to_custom))(self.keyboard_commands.choose_customization)
        self.dp.message(Form.set_timing_dark, F.text.in_(self.language.back_to_custom))(self.keyboard_commands.choose_customization)
        self.dp.message(Form.set_timing_light, F.text.in_(self.language.back_to_custom))(self.keyboard_commands.choose_customization)
        self.dp.message(F.web_app_data)(self.user_commands.get_web_app_data)
        self.dp.message(Form.set_alignment_dark, F.web_app_data)(self.color.advanced_custom_color)
        self.dp.message(Form.set_alignment_light, F.web_app_data)(self.color.advanced_custom_color)
        self.dp.message(Form.set_data_dark, F.web_app_data)(self.color.advanced_custom_color)
        self.dp.message(Form.set_data_light, F.web_app_data)(self.color.advanced_custom_color)
        self.dp.message(Form.set_finder_dark, F.web_app_data)(self.color.advanced_custom_color)
        self.dp.message(Form.set_finder_light, F.web_app_data)(self.color.advanced_custom_color)
        self.dp.message(Form.set_format_dark, F.web_app_data)(self.color.advanced_custom_color)
        self.dp.message(Form.set_format_light, F.web_app_data)(self.color.advanced_custom_color)
        self.dp.message(Form.set_quiet_zone, F.web_app_data)(self.color.advanced_custom_color)
        self.dp.message(Form.set_separator, F.web_app_data)(self.color.advanced_custom_color)
        self.dp.message(Form.set_timing_dark, F.web_app_data)(self.color.advanced_custom_color)
        self.dp.message(Form.set_timing_light, F.web_app_data)(self.color.advanced_custom_color)

        #command
        self.dp.message(F.new_chat_members)
        self.dp.message(CommandStart())(self.user_commands.command_start_handler)
        self.dp.message(Command('help'))(self.user_commands.help_command)
        self.dp.message(F.text == '/user')(self.admin_command.user_commands)

        #admin command
        self.dp.callback_query(lambda c: c.data == 'users')(self.admin_command.process_callback_view_users)
        self.dp.callback_query(lambda c: c.data == 'clean')(self.admin_command.clean_inactive_users)    
        self.dp.callback_query(lambda c: c.data == 'repair')(self.admin_command.wait_document)    
        self.dp.callback_query(F.data == 'cancel')(self.keyboard_commands.inline_cancel_command)
        self.dp.message(Form.set_repair, F.document)(self.admin_command.repair_user_id)
        # self.dp.message(Form.set_user_die)(self.commands.delate_users)

        #create qr
        self.dp.message(F.text.in_(self.language.visual_qr_reply))(self.user_commands.visual_qr)
        self.dp.message(F.text.in_(self.language.normal_qr_reply))(self.user_commands.normal_qr)
        #self.dp.message(F.text.in_(self.language.create_qr_ai))(self.create_qr.ai_qr)
        self.dp.callback_query(F.data == 'save_message')(self.keyboard_commands.message_saved)
        self.dp.message(F.text == 'Advanced Custom ⚙️')(self.keyboard_commands.choose_customization)
        self.dp.callback_query(F.data.startswith('custom:'))(self.keyboard_commands.advanced_custom)
        self.dp.callback_query(F.data == 'view')(self.user_commands.create_advanced_qr)

        #language_setting
        self.dp.message(F.text.in_(self.language.language_setting_reply))(self.keyboard_commands.choose_language)
        self.dp.callback_query(F.data.startswith('code'))(self.keyboard_commands.language_settend)

        #ads
        self.dp.callback_query(lambda c: c.data == 'ads')(self.admin_command.recive_ads)
        self.dp.callback_query(F.data == "set_ads")(self.admin_command.set_place_ads)
        self.dp.message(Form.set_ads)(self.admin_command.send_ads)
        self.dp.message(Form.set_place_ads)(self.admin_command.recive_place_ads)

        self.dp.message(Form.Text_VisualQR, F.web_app_data | F.text)(self.input_user.set_image_qr)
        self.dp.message(Form.Text_VisualQR, F.photo)(self.input_user.convert_image_url)
        self.dp.message(Form.Image_VisualQR, F.photo | F.document | F.animation)(self.user_commands.recive_image)
        self.dp.message(Form.Image_VisualQR)(self.keyboard_commands.cancel_operation)
        self.dp.message(F.photo | F.document)(self.reader.read_process)
        self.dp.message(Form.set_bg_color, F.web_app_data)(self.color.recive_web_color)
        self.dp.message(Form.set_bg_color)(self.keyboard_commands.cancel_operation)
        self.dp.message(F.text.in_(self.language.custom_background_reply))(self.tutorial.tutorial_light)
        self.dp.message(Form.set_background, F.web_app_data)(self.color.handle_set_background)
        self.dp.message(Form.set_background)(self.keyboard_commands.background_command)
        self.dp.message(F.text.in_(self.language.custom_foreground_reply))(self.tutorial.tutorial_dark)
        self.dp.message(Form.set_foreground, F.web_app_data)(self.color.handle_set_foreground)
        self.dp.message(Form.set_foreground)(self.keyboard_commands.foreground_command)
        self.dp.message(F.text)(self.user_commands.handle_circle_qr)   
        self.dp.message(F.text.in_(self.language.version))
    
        
        
                    
      
            