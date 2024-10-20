from aiogram.methods import send_photo
# from pyzbar.pyzbar import decode
import os
from pdf417decoder import PDF417Decoder
#import numpy as np
import asyncio
import zxingcpp
import segno
from datetime import datetime
from segno import helpers
import logging
from aiogram import types
from PIL import Image, ImageColor, ImageOps ,ImageDraw, ImageFont, ImageFilter
import qrcode
from qrcode.image.styledpil import StyledPilImage
from .language import Language
from . import instance
from . import config
from .user import UserInfo

from qrcode.image.styles.moduledrawers import (
    CircleModuleDrawer, SquareModuleDrawer
)
import uuid
from io import BytesIO
from aiogram.types.input_file import InputFile
from .image import FileManager

class QR:
    def __init__(self):
        self.bot = instance.bot
        self.admin_id = config.admin_id
        self.image_instance = FileManager()

    async def readqr(self, file_name, user_id): 
        try:
            name, file_extension = os.path.splitext(file_name)      
            if file_extension.lower() not in ['.jpg', '.jpeg']:
                converted_file_name = self.convert_to_jpg(file_name)
                if converted_file_name:
                    file_name = converted_file_name
                
            image = Image.open(file_name)
            inverted_image = ImageOps.invert(image)
       
            qr_results = await asyncio.gather( #Decodifica prima i QR code con pyzbar
                self.decode_qr(image),
                self.decode_qr(inverted_image),
            )
            if not any(qr_results): #Se non viene trovato alcun QR code, decodifica i codici in zxing-cpp
                other_results = await asyncio.gather(
                    self.decode_pdf417(image),
                    self.decode_barcode(image),
                )
                results = qr_results + other_results 
            else:
                results = qr_results 
            copy_file = f"{name}.jpg"
            if os.path.exists(copy_file) and copy_file.startswith("qr_"):
                os.remove(copy_file)
            return results
        except Exception as ex:
            logging.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await self.bot.send_message(self.admin_id, f"{user_id}:{ex}")

    # def pdf_to_images(input_pdf_path, output_image_path):
    #     images = convert_from_path(input_pdf_path, output_folder=output_image_path, fmt='jpeg')
    #     return images

    def convert_to_jpg(self, file_path):
        try:
            image = Image.open(file_path)
            jpg_path = os.path.splitext(file_path)[0] + '.jpg'
            image.convert('RGB').save(jpg_path)
            # if os.path.exists(file_path):
            #     os.remove(file_path)
            return jpg_path
        except Exception as e:
            print(f"Errore durante la conversione in JPG: {e}")
            return None

    async def decode_qr(self, image):
        decoded_objects = decode(image)
        results = {}
        if decoded_objects:
            for obj in decoded_objects:
                cleaned_data = obj.data.decode("utf-8")
                if obj.type not in results:
                    results[obj.type] = []
                results[obj.type].append(cleaned_data)
        return results
                
    async def decode_barcode(self, image):
        decoded_object = zxingcpp.read_barcode(image) #Utilizza ZXing-C++ per decodificare i Barcode e anche QR code
        if decoded_object:
            format_type = str(decoded_object.format).replace("BarcodeFormat.", "")
            return f'Type: {format_type}, Data: {decoded_object.text}'

    async def decode_pdf417(self, image): #Utilizza PDF417Decoder per decodificare i PDF417
        PDFDecoder = PDF417Decoder(image)
        if PDFDecoder.decode() > 0:
            cleaned_data = PDFDecoder.barcode_data_index_to_string(0)
            return f'Type: PDF417, Data: {cleaned_data}'
        
    def write_artistic_qr(self, user_id, text, dark, light, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version, image, visual_qr=True):
        try:      
            color_dark = tuple(map(int, dark.split(',')))
            color_light = tuple(map(int, light.split(',')))
            color_alignment_dark =  tuple(map(int, alignment_dark.split(',')))
            color_alignment_light =  tuple(map(int, alignment_light.split(',')))
            color_data_dark =  tuple(map(int, data_dark.split(',')))
            color_data_light =  tuple(map(int, data_light.split(',')))
            color_finder_dark =  tuple(map(int, finder_dark.split(',')))
            color_finder_light =  tuple(map(int, finder_light.split(',')))
            quiet_zone =  tuple(map(int, quiet_zone.split(',')))
            separator =  tuple(map(int, separator.split(',')))
            timing_dark =  tuple(map(int, timing_dark.split(',')))
            timing_light =  tuple(map(int, timing_light.split(',')))
            version_dark =  tuple(map(int, version_dark.split(',')))
            version_light =  tuple(map(int, version_light.split(',')))   

            border_width = 10
            if version > 1:
                code = segno.make(text, error='h', version=version)   
            else:
                code = segno.make(text, error='h')
                                    
            if visual_qr:
                code.to_artistic(background=image, target=image,scale=10, dark=color_dark, light=color_light, data_dark=color_data_dark, data_light=color_data_light, alignment_dark=color_alignment_dark,
                                    alignment_light= color_alignment_light, finder_dark=color_finder_dark, finder_light = color_finder_light, quiet_zone=quiet_zone,
                                    separator=separator, timing_dark=timing_dark, timing_light=timing_light, version_dark=version_dark, version_light=version_light)   
        except Exception as ex:
            logging.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
    
    def write_normal_qr(self, text, dark, light, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version):
        try:        
            color_dark = tuple(map(int, dark.split(',')))
            color_light = tuple(map(int, light.split(',')))
            color_alignment_dark =  tuple(map(int, alignment_dark.split(',')))
            color_alignment_light =  tuple(map(int, alignment_light.split(',')))
            color_data_dark =  tuple(map(int, data_dark.split(',')))
            color_data_light =  tuple(map(int, data_light.split(',')))
            color_finder_dark =  tuple(map(int, finder_dark.split(',')))
            color_finder_light =  tuple(map(int, finder_light.split(',')))
            quiet_zone =  tuple(map(int, quiet_zone.split(',')))
            separator =  tuple(map(int, separator.split(',')))
            timing_dark =  tuple(map(int, timing_dark.split(',')))
            timing_light =  tuple(map(int, timing_light.split(',')))
            version_dark =  tuple(map(int, version_dark.split(',')))
            version_light =  tuple(map(int, version_light.split(',')))   

            border_width = 10
            if version > 1:
                code = segno.make(text, error='h', version=version)   
            else:
                code = segno.make(text, error='h')
                                    
            image = f"qr_{uuid.uuid4()}.png"
            img = code.to_pil(scale=10, dark=color_dark, light=color_light, data_dark=color_data_dark, data_light=color_data_light, alignment_dark=color_alignment_dark,
                                alignment_light= color_alignment_light, finder_dark=color_finder_dark, finder_light = color_finder_light, quiet_zone=quiet_zone,
                                separator=separator, timing_dark=timing_dark, timing_light=timing_light, version_dark=version_dark, version_light=version_light)
            
            bg = Image.new('RGB', img.size, color_data_light)
                    
            result = Image.alpha_composite(bg.convert('RGBA'), img.convert('RGBA')).convert('RGB') ##Sovrapponi il QR code sull'immagine di sfondo
            border = Image.new('RGB', (img.width + 2*border_width, img.height + 2*border_width), color_data_light)
                    
            border.paste(img, (border_width, border_width))
            border.save(image)
            return image
        except Exception as ex:
            logging.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            
    def check_qr_result(self, result):
        if (
            isinstance(result, list) and
            len(result) == 4 and
            result[0] == {} and
            result[1] == {} and
            result[2] is None and
            result[3] is None
        ):
            return False
        return True    
                
    def make_geo_qr(self, latitude, longitude):
        code = f'https://www.google.com/maps?q={latitude},{longitude}'
        qrcode = segno.make(code, error='H')
        return qrcode

    async def write_geo(self, chat_id, latitude, longitude):
        qrcode = self.make_geo_qr(latitude, longitude)

        # Salva il QR code come immagine
        img_path = 'qr_code.png'
        qrcode.save(img_path, scale=10)

        # Invia l'immagine
        with open(img_path, "rb") as img_file:
            await self.bot.send_photo(chat_id, img_file)

        # Rimuovi l'immagine
        os.remove(img_path)

        return
                
    async def QR_Circle(self, text, message):
        info = UserInfo(message)
        language = Language()
        count = len(text)
        if count > 115:
                                    
            text = language.max_capacity(info.language)
            await self.bot.send_message(info.user_id, text)
            return
        else:
            qr = qrcode.QRCode(
                version=10,  # https://github.com/lincolnloop/python-qrcode/blob/df139670ac44382d4b70820edbe0a9bfda9072aa/qrcode/util.py#L183
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=18,
                mask_pattern=4,  # https://www.thonky.com/qr-code-tutorial/mask-patterns,
            )
            qr.add_data(text)
            qr.make(fit=True)

            img = qr.make_image(
                fill_color="white",
                back_color=None,
                image_factory=StyledPilImage,
                module_drawer=CircleModuleDrawer(resample_method=None),
                eye_drawer=SquareModuleDrawer(),
            )

            width, height = img.size
            left = 0
            top = height // 3
            right = width
            bottom = 2 * height//3

            cropped_section = img.crop((left, top, right, bottom))

            rotated_crop = cropped_section.copy()
            rotated_crop = rotated_crop.rotate(90, expand=True)

            img.paste(cropped_section, (0, -cropped_section.size[1]//2 + 20 ))
                
            img.paste(cropped_section, (0, img.size[1] - cropped_section.size[1]//2 -20 )) # fill bottom                
            img.paste(rotated_crop, (-rotated_crop.size[0]//2 + 20, 0)) # fill left
            img.paste(rotated_crop, (img.size[0] - rotated_crop.size[0]//2 - 20, 0)) # fill right
            draw = ImageDraw.Draw(img)
            draw.ellipse(
                (30, 30, img.size[1]-30, img.size[1]-30),
                fill = None,
                outline ='black',
                width=30
            )
            draw.ellipse(
                (-rotated_crop.size[0],
                    -cropped_section.size[1],
                    img.size[1] + rotated_crop.size[0],
                    img.size[1] + cropped_section.size[1]
                    ),
                fill = None,
                outline ='white',
                width=340
            )            
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            img_file = types.BufferedInputFile(img_byte_arr, filename=f"qr_{uuid.uuid4()}.png")
            return img_file
