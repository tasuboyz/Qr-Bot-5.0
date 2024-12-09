from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.types.web_app_info import WebAppInfo
import os
from .language import Language
from .user import UserInfo

class Keyboard_Manager:
    def __init__(self):
        self.scan_url = 'https://mboretto.github.io/easy-qr-scan-bot/'
        self.test_scan_url = 'https://easyqrscanbot.netlify.app/'
        self.color_url = 'https://python-telegram-bot.org/static/webappbot'
        self.premium_bot = 'https://t.me/TasuPremiumBot'
        self.qr_info_url = 'https://tasuboyz.github.io/Qr-Info-TWA/'
        self.qr_interface = 'https://tasuboyz.github.io/Qr-interface/'
        self.lang = Language()
        
    def create_start_reply_keyboard(self, data):
        info = UserInfo(data)
        language_code = info.language
        visual_qr = self.lang.visual_qr(language_code)
        normal_qr = self.lang.normal_qr(language_code)
        scan_qr = self.lang.scan_qr(language_code)
        lang_setting = self.lang.language_setting(language_code)
        #ai_qrcode = self.lang.ai_qrcode(language_code)
        customize_qr = self.lang.customize_qr(language_code)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [
                KeyboardButton(text=customize_qr, web_app=WebAppInfo(url=self.qr_interface)) 
            ],
            # [
            #     KeyboardButton(text=ai_qrcode)
            # ],
            [
                KeyboardButton(text=lang_setting)
            ],
            [
                KeyboardButton(text=scan_qr, web_app=WebAppInfo(url=self.scan_url)) 
            ]                                    
        ])
        return keyboard

    def create_url_app(self, url: str, message: Message):             
        info = UserInfo(message)
        user_id = message.from_user.id
        language_code = info.language
        open_link = self.lang.open_link(language_code)
        # if 'https' in url:           
        #     keyboard = InlineKeyboardMarkup(inline_keyboard=[
        #         [InlineKeyboardButton(text=open_link, web_app=WebAppInfo(url=url))]
        #     ]) 
        #     return keyboard   
        if url.startswith('http'):           
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=open_link, url=url)]
            ])  
            return keyboard   
        else:
            raise ValueError("Invalid URL 🚫")

    def color_chooser(self, message: Message):
        info = UserInfo(message)
        user_id = message.from_user.id
        language_code = info.language
        cancel = self.lang.cancel(language_code)
        choose_color = self.lang.choose_color(language_code)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [
                KeyboardButton(text=choose_color, web_app=WebAppInfo(url=self.color_url))
            ],
            [
                KeyboardButton(text=cancel) 
            ]                                    
        ])
        return keyboard
    
    def create_color_reply_keyboard(self, message: Message, save_color, AIremove):        
        info = UserInfo(message)
        user_id = message.from_user.id
        language_code = info.language
        cancel = self.lang.cancel(language_code)
        choose_color = self.lang.choose_color(language_code)
        previous_color = self.lang.previous_color(language_code)
        AIremover_ON = '🤖 AI Remover 🚫'
        AIremover_OFF = '🤖 AI Remover ✅'
        back = self.lang.back(language_code)

        color_button = KeyboardButton(text=choose_color, web_app=WebAppInfo(url=self.color_url))
        previous_color_button = KeyboardButton(text=previous_color)
        AIremover_button = KeyboardButton(text=AIremover_ON if AIremove else AIremover_OFF)
        back_button = KeyboardButton(text=back)
        cancel_button = KeyboardButton(text=cancel)

        if AIremove is not None:
            if save_color is not None:
                keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
                    #[color_button, previous_color_button],
                    [color_button],
                    [AIremover_button],
                    [back_button],
                    [cancel_button]
                ])
            else:
                keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
                    [color_button],
                    [AIremover_button],
                    [back_button],
                    [cancel_button]
                ])
        else:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
                #[color_button, previous_color_button],
                [color_button],
                [back_button],
                [cancel_button]
            ])
        return keyboard
    
    def mecard(self, message: Message, saved_data="None"):
        info = UserInfo(message)
        user_id = message.from_user.id
        language_code = info.language
        cancel = self.lang.cancel(language_code)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [
                KeyboardButton(text=saved_data)
            ],
            [
                KeyboardButton(text="Contact info 📱 (Beta)", web_app=WebAppInfo(url=self.qr_info_url))
            ],
            [
                KeyboardButton(text="Wifi Qr 🛜 (Beta)", web_app=WebAppInfo(url=self.qr_wifi))
            ],
            [
                KeyboardButton(text=cancel) 
            ]                                    
        ])
        return keyboard
    
    def cancel(self, message: Message):
        info = UserInfo(message)
        user_id = message.from_user.id
        language_code = info.language
        cancel = self.lang.cancel(language_code)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [
                KeyboardButton(text=cancel) 
            ]                                    
        ])
        return keyboard
    
    def custom(self, message: Message, qr):
        info = UserInfo(message)
        user_id = message.from_user.id
        language_code = info.language
        confirm = self.lang.confirm(language_code, qr)
        custom_background = self.lang.custom_background(language_code)
        custom_foreground = self.lang.custom_foreground(language_code)
        version = self.lang.custom_version(language_code)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [
                # KeyboardButton(text=custom_foreground),
                KeyboardButton(text=custom_background) 
            ],
            # [
            #     KeyboardButton(text="Version") 
            # ],
            [
                # KeyboardButton(text="Advanced Custom ⚙️") 
            ],
            [
                KeyboardButton(text=confirm) 
            ]
        ])
        return keyboard

    def language_setting(self):
        keyboard_buttons = []
        keyboard_buttons.append([InlineKeyboardButton(text="Italiano 🇮🇹", callback_data="code:it"),
                                 InlineKeyboardButton(text="Spanish 🇪🇦", callback_data="code:es"),
                                 InlineKeyboardButton(text="भारतीय 🇮🇳", callback_data="code:hi")])
        keyboard_buttons.append([InlineKeyboardButton(text="English 🇬🇧", callback_data="code:en"),
                                 InlineKeyboardButton(text="Français 🇫🇷", callback_data="code:fr"),
                                 InlineKeyboardButton(text="Deutsch 🇩🇪", callback_data="code:de")])
        keyboard_buttons.append([InlineKeyboardButton(text="Русский 🇷🇺", callback_data="code:ru"),
                                 InlineKeyboardButton(text="Українська 🇺🇦", callback_data="code:uk"),
                                 InlineKeyboardButton(text="中文 🇨🇳", callback_data="code:zh")])
        keyboard_buttons.append([InlineKeyboardButton(text="العربية🇸🇦", callback_data="code:ar")])
        keyboard_buttons.append([InlineKeyboardButton(text="Cancel ❌", callback_data="cancel")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        return keyboard
    
    def save_message_keyboard(self, message):
        keyboard = []               
        info = UserInfo(message)
        language_code = info.language
        save = self.lang.save_action(language_code)
        keyboard.append([InlineKeyboardButton(text=save, callback_data="save_message")])       
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard
    
    def premium_keyboard(self, message):
        keyboard = []               
        info = UserInfo(message)
        language_code = info.language
        buy_premium = self.lang.buy_premium_pack(language_code)
        keyboard.append([InlineKeyboardButton(text=buy_premium, url=self.premium_bot)])       
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard

############################################################################################## Versione Sperimentale
    def create_version(self):
        keyboard = []
        columns = 6
        keyboard = InlineKeyboardMarkup(row_width=columns)  # Imposta il numero di colonne desiderato
        row_buttons = []

        for version in range(1, 39):
            row_buttons.append([InlineKeyboardButton(text = str(version), callback_data=f"version:{version}")])
            
            if len(row_buttons) == columns:
                keyboard.add(*row_buttons) # Aggiungi i pulsanti alla tastiera ogni 'columns' iterazioni
                row_buttons = []
        
        if row_buttons:
            keyboard.add(*row_buttons) # Aggiungi eventuali pulsanti rimasti (se il numero totale non è un multiplo di 'columns')

        return keyboard

    def create_user_keyboard(self):
        keyboard = []               
        keyboard.append([InlineKeyboardButton(text="📦 Invia Messaggio agli Utenti", callback_data="send_message")])       
        keyboard.append([InlineKeyboardButton(text="🔍 Dettagli utenze attive", callback_data="users")])
        keyboard.append([InlineKeyboardButton(text="🛠 Riparazione utenti", callback_data="repair")])
        keyboard.append([InlineKeyboardButton(text="🧹 Pulizia Utenti", callback_data="clean")])
        keyboard.append([InlineKeyboardButton(text="Send Ads 📮", callback_data="ads")])
        keyboard.append([InlineKeyboardButton(text="Set Ads 🎬", callback_data="set_ads")])
        keyboard.append([InlineKeyboardButton(text="Annulla ❌", callback_data="cancel")])

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard

    def advanced_setting(self, alignment_dark="0,0,0", alignment_light="255,255,255", data_dark="0,0,0", data_light="255,255,255", finder_dark="0,0,0", finder_light="255,255,255", format_dark="0,0,0", format_light="255,255,255", quiet_zone="0,0,0", separator="255,255,255", timing_dark="0,0,0", timing_light="255,255,255"):
        
        yes = "✅"
        no = "🚫"   
        options = [
            (f"alignment_dark {yes if not self.is_black_or_white(alignment_dark) else no}", 
            f"alignment_light {yes if not self.is_black_or_white(alignment_light) else no}"),
            (f"data_dark {yes if not self.is_black_or_white(data_dark) else no}", 
            f"data_light {yes if not self.is_black_or_white(data_light) else no}"),
            (f"finder_dark {yes if not self.is_black_or_white(finder_dark) else no}", 
            f"finder_light {yes if not self.is_black_or_white(finder_light) else no}"),
            (f"format_dark {yes if not self.is_black_or_white(format_dark) else no}", 
            f"format_light {yes if not self.is_black_or_white(format_light) else no}"),
            (f"quiet_zone {yes if not self.is_black_or_white(quiet_zone) else no}", 
            f"separator {yes if not self.is_black_or_white(separator) else no}"),
            (f"timing_dark {yes if not self.is_black_or_white(timing_dark) else no}", 
            f"timing_light {yes if not self.is_black_or_white(timing_light) else no}")
        ]
        keyboard = [[InlineKeyboardButton(text=opt[0], callback_data=f"custom:{opt[0]}"),
                    InlineKeyboardButton(text=opt[1], callback_data=f"custom:{opt[1]}")]
                    for opt in options]
        keyboard.append([InlineKeyboardButton(text="View Result 👀", callback_data="view")])
        keyboard.append([InlineKeyboardButton(text="Annulla ❌", callback_data="cancel")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def is_black_or_white(self, color):
            return color == "0,0,0" or color == "255,255,255"



