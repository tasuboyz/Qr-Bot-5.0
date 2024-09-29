from PIL import Image, ImageColor, ImageOps ,ImageDraw, ImageFont, ImageFilter, ImageSequence
from rembg import remove
import numpy as np
import io
import os
import time
from moviepy.editor import VideoFileClip
import random
import uuid
from .logger_config import logger
import glob
from .user import UserInfo
from .language import Language
from . import instance
from .config import admin_id
from .db import Database

class FileManager: # crea una classe per gestire i colori e le impostazioni del QR
    def __init__(self):
        self.bot = instance.bot
        self.admin_id = admin_id
        self.lang = Language()

    def resize(self, file_path, fill_color):
        try:
            color = tuple(map(int, fill_color.split(',')))
            if file_path.endswith(('.jpg', '.jpeg')):  # aggiungi qui altri formati di immagine se necessario
                im = Image.open(file_path)            
                if im.size[0] != im.size[1]: #Controlla se l'immagine è quadrata
                    im_square = self.make_square(im, color)
                    im_square.save(file_path)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)

    def resize_gif(self, file_path, fill_color):
        try:
            color = tuple(map(int, fill_color.split(',')))
            if file_path.endswith('.gif'):  # controlla se il file è una gif
                im = Image.open(file_path)
                frames = [self.make_square(f.copy(), color) for f in ImageSequence.Iterator(im)]
                
                frames[0].save(file_path, format='GIF', append_images=frames[1:], save_all=True, loop=0)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
                    
    def make_square(self, im, fill_color):
        try:
            min_size=256
            x, y = im.size
            size = max(min_size, x, y)
            new_im = Image.new('RGB', (size, size), fill_color)
            new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
            return new_im
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)

    def background_remover(self, file_name, color):
        try:
            background_color = tuple(map(int, color.split(',')))
            base_name = os.path.splitext(file_name)[0]  # Ottieni il nome del file senza estensione
            output_path = f'{base_name}.png'  # Aggiungi '.png'

            with open(file_name, 'rb') as img_file:
                img = img_file.read()

            result = remove(img)

            img = Image.open(io.BytesIO(result)).convert("RGBA")
            background = Image.new('RGBA', img.size, background_color)
    
            img_with_background = Image.alpha_composite(background, img)# Combina l'immagine e lo sfondo

            img_with_background.save(output_path)  # Salva l'immagine come PNG

            jpeg_path = f'{base_name}.jpg'  # Usa lo stesso nome base, ma con estensione '.jpg'
            img_jpeg = img_with_background.convert('RGB')  # Rimuovi il canale alfa
            img_jpeg.save(jpeg_path, 'JPEG')  # Salva l'immagine come JPEG
            # os.remove(output_path)   
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)

    def generate_random_filename(self, file_path):
        file_name, file_extension = os.path.splitext(file_path)
        random_suffix = random.randint(1000, 9999)
        return f"{file_name}_{random_suffix}{file_extension}"

    def check_file_exists(self, file_path):
        while os.path.exists(file_path):
            file_path = self.generate_random_filename(file_path)
        return file_path
            
    def convert_mp4(self, file_mp4):
        clip = VideoFileClip(file_mp4)
        file_gif = os.path.splitext(file_mp4)[0] + '.gif'
        clip.write_gif(file_gif)
        if os.path.exists(file_mp4):
            os.remove(file_mp4)
    
    async def check_image(self, file_name, message, keyboard):
        info = UserInfo(message)
        language_code = info.language
        file_not_valid = self.lang.file_not_valid(language_code)
        try:
            Image.open(file_name)
        except IOError:
            await message.reply(file_not_valid, reply_markup=keyboard)                    
            os.remove(file_name)
            return True
            
    def remove_file_if_exists(self, file, origianl_file, file_jpg):     
        for file in glob.glob(file + ".*"):
            if os.path.exists(file):
                os.remove(file)        
        file = r"UserImage/"f"{file}"
        for file in glob.glob(file + ".*"):
            if os.path.exists(file):
                os.remove(file)
                    
    def get_file_details(self, file_name: str):
        # Ottieni i dettagli del file
        nome_completo = os.path.basename(file_name).split(".")[0]
        percorso = os.path.dirname(os.path.abspath(file_name)) #visualizza percorso file
        file = file_name.split(".")[0]
        extention = file_name.split(".")[-1]
        file_jpg = f'{percorso}//{file}.jpg'
        return nome_completo, file_name, extention, file_jpg
            
class FileMod():
    def __init__(self):
        self.bot= instance.bot
        self.blocked_users = instance.blocked_users
        self.db = Database()
        self.image = FileManager()

    def delate(self, user_id):
            file_name = self.db.get_image(user_id)    
            if file_name != None:
                # file, extention, file_jpg = self.get_file_details(file_name)
                nome_completo, _, extention, file_jpg = self.image.get_file_details(file_name)
                self.image.remove_file_if_exists(nome_completo, extention, file_jpg) #elimina file
                self.db.delate_image(user_id)
                self.db.delate_colors(user_id)
                
    def cleanup(self, img_path):
            name ,estensione = os.path.splitext(img_path)
            percorso = os.path.dirname(os.path.abspath(img_path))
            file_path = f'{percorso}\{img_path}'
            self.image.remove_file_if_exists(name, img_path, file_path) #elimina file    
            
    async def write_ids(self, results):
          info = UserInfo(None)
          with open('ids.txt', 'w') as file:
            for result in results:
                # status = await info.get_vip_member(result[0])
                # if status != 'member':
                    file.write(str(result[0]) + '\n')

    def me_card_compound(self, web_data):
        title = web_data['title']
        surname = web_data['surname']
        caselle = web_data['caselle']

        mecard = f"MECARD:N:{title},{surname};"

        for casella in caselle:
            url = casella['url']
            email = casella['email']
            phone = casella['phone']

            mecard += f"URL:{url};EMAIL:{email};TEL:{phone};"
        return mecard