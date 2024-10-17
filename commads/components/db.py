import sqlite3
import re
from commads.components.logger_config import logger
import time
import mysql.connector

class Database():
    def __init__(self):
        #self.conn = sqlite3.connect('qruser_malformed.db')
        # self.hive_conn = mysql.connector.connect(
        #     host='192.168.1.9',
        #     user='khadas',
        #     password='Alecinko03',
        #     database='cur8_hive_database'
        # )
        # self.c_hive = self.hive_conn.cursor()

        self.conn = sqlite3.connect('qruser.db')
        self.c = self.conn.cursor()            
        #tables
        self.LANGUAGE = "LANGUAGE"
        self.SAVED_TEXT = "SAVED_TEXT"
        self.ADS_TEXT = 'ADS_TEXT'
        self.USER_ACCOUNT = 'USER_ACCOUNT'
        #columns
        self.language_code = "language_code"
        self.user_id = "user_id"
        self.saved_text = "saved_text"
        self.ads_text = 'ads_text'
        self.username = 'username'
        self.account = "account"
        self.password = 'password'
    pass
        
    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS TEXT (user_id INTEGER PRIMARY KEY, text TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS AI_MODE (user_id INTEGER PRIMARY KEY, remover BOOL)''')  
        self.c.execute('''CREATE TABLE IF NOT EXISTS user_file (user_id INTEGER PRIMARY KEY, file_name TEXT)''') 
        self.c.execute('''CREATE TABLE IF NOT EXISTS COLOR (user_id INTEGER PRIMARY KEY, color TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS MESSAGE (chat_id INTEGER PRIMARY KEY, photo_id INT, custom_main INT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS QR (user_id INTEGER PRIMARY KEY, qr BOOL)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS user_settings
        (
            user_id INTEGER PRIMARY KEY,
            foreground_color TEXT,
            background_color TEXT,
            alignment_dark TEXT,
            alignment_light TEXT,
            data_dark TEXT,
            data_light TEXT,
            finder_dark TEXT,
            finder_light TEXT,
            quiet_zone TEXT,
            separator TEXT,
            timing_dark TEXT,
            timing_light TEXT,
            version_dark TEXT,
            version_light TEXT,
            version INT
        )''')
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.LANGUAGE} ({self.user_id} INT PRIMARY KEY, {self.language_code} TEXT)''')
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.SAVED_TEXT} ({self.user_id} INTEGER PRIMARY KEY, {self.saved_text} TEXT)''')
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.ADS_TEXT} ({self.user_id} INTEGER PRIMARY KEY, {self.ads_text} TEXT)''')
        self.conn.commit()
        
    def copy_data(self):
        # Aggiungi il nuovo database
        self.c.execute("ATTACH DATABASE 'qruser.db' AS qruser")

        # # Copia dati per ogni tabella
        tables = ["users"]
        for table in tables:
            self.c.execute(f"CREATE TABLE qruser.{table} AS SELECT * FROM {table}")

        # Copia dati per la tabella della lingua specifica
        #self.c.execute(f"CREATE TABLE new_db.{self.LANGUAGE} AS SELECT * FROM {self.LANGUAGE}")

        # Scollega il nuovo database
        self.c.execute("DETACH DATABASE 'qruser'")
        self.conn.commit()

    def insert_user_data(self, user_id, username):
        self.c.execute("INSERT OR REPLACE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        self.conn.commit()

    def insert_all_users(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                user_id = line.strip()  # Rimuove i caratteri di spazio bianco alla fine di ogni riga
                username = 'username'  # Sostituisci con il metodo per ottenere il nome utente
                self.insert_user_data(user_id, username)
    
    def user_text(self, user_id, text):
        self.c.execute('''REPLACE INTO TEXT (user_id, text) VALUES (?, ?)''', (user_id, text))
        self.conn.commit()
        
    def get_user_text(self, user_id):
        self.c.execute('''SELECT text FROM TEXT WHERE user_id = ?''', (user_id,))
        result = self.c.fetchone()
        self.conn.commit()
        return result[0] if result else (None)
    
    def delate_temp(self, user_id):
        self.c.execute("DELETE FROM TEXT WHERE user_id = ?", (user_id,)) 
        self.conn.commit()

    def qr_table(self, user_id, qr): 
        self.c.execute('''REPLACE INTO QR (user_id, qr) VALUES (?, ?)''', 
                        (user_id, qr))
        self.conn.commit()
        return
    
    def save_image(self, user_id, file_name):
        self.c.execute('''INSERT OR REPLACE INTO user_file (user_id, file_name) VALUES (?, ?) ''', (user_id, file_name))
        self.conn.commit()
        
    def get_image(self, user_id):
        self.c.execute('''SELECT file_name FROM user_file WHERE user_id = ?''', (user_id,))
        result = self.c.fetchone()
        self.conn.commit()
        return result[0] if result else (None)
    
    def get_user_by_image(self, file_name):
        self.c.execute('''SELECT user_id FROM user_fileWHERE file_name = ?''', (file_name,))
        result = self.c.fetchone()
        self.conn.commit()
        return result[0] if result else (None)
    
    def delate_image(self, user_id):
        self.c.execute("DELETE FROM user_file WHERE user_id = ?", (user_id,)) 
        self.conn.commit()
    
    def get_qr(self, chat_id): 
        self.c.execute('''SELECT qr FROM QR WHERE user_id = ?''', (chat_id,))
        row = self.c.fetchone()
        self.conn.commit()
        if row != None:
            return row[0]
        else:
            return None
        
    def save_settings(self, user_id, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version):
        self.c.execute('''
            INSERT OR REPLACE INTO user_settings (user_id, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version))
        self.conn.commit()

    def get_settings(self, user_id):
        self.c.execute('''
            SELECT foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version FROM user_settings
            WHERE user_id = ?
        ''', (user_id,))
        result = self.c.fetchone()
        self.conn.commit()
        return result if result else (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
    
    def default_setting(self, user_id):
        user_id = int(user_id)
        DEFAULT_LIGHT_COLOR = '255,255,255'
        DEFAULT_DARK_COLOR = '0,0,0'
        DEFAULT_VERSION = 1
        self.c.execute('''
            INSERT OR REPLACE INTO user_settings (user_id, foreground_color, background_color, alignment_dark, alignment_light, data_dark, data_light, finder_dark, finder_light, quiet_zone, separator, timing_dark, timing_light, version_dark, version_light, version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, DEFAULT_DARK_COLOR, DEFAULT_LIGHT_COLOR, DEFAULT_DARK_COLOR, DEFAULT_LIGHT_COLOR, DEFAULT_DARK_COLOR, DEFAULT_LIGHT_COLOR, DEFAULT_DARK_COLOR, DEFAULT_LIGHT_COLOR, DEFAULT_LIGHT_COLOR, DEFAULT_LIGHT_COLOR, DEFAULT_DARK_COLOR, DEFAULT_LIGHT_COLOR, DEFAULT_DARK_COLOR, DEFAULT_LIGHT_COLOR, DEFAULT_VERSION))
        self.conn.commit()   
        
    def AI_Remover(self, user_id, remover):
        self.c.execute('''INSERT OR REPLACE INTO AI_MODE (user_id, remover) VALUES (?, ?) ''', (user_id, remover))
        self.conn.commit()
        
    def view_remover_state(self, user_id):
        self.c.execute('SELECT remover FROM AI_MODE WHERE user_id = ?', (user_id,)) # Ottieni lo stato personalizzato dell' l'utente
        row = self.c.fetchone()
        self.conn.commit()
        if row is not None:
            if row[0] != 0:
                return row[0]
            else:
                return None
        return None
        
    def delate_remover_state(self, user_id):
        self.c.execute("DELETE FROM AI_MODE WHERE user_id = ?", (user_id,)) 
        self.conn.commit()
        
    def get_color_from_data(self, user_id):
        self.c.execute('''SELECT color FROM COLOR WHERE user_id = ?''', (user_id,))
        row = self.c.fetchone()
        self.conn.commit()
        if row is not None:
            return row[0]
        else:
            return None  # o qualsiasi valore predefinito
    
    def save_color_in_settings(self, user_id, color): # crea un metodo per salvare il colore nelle impostazioni dell'utente
        self.c.execute('''INSERT OR REPLACE INTO COLOR (user_id, color) VALUES (?, ?)''',
                        (user_id, color))
        self.conn.commit()
        return
    
    def delate_colors(self, user_id): # crea un metodo per scrivere il QR con i colori appropriati
        self.c.execute("DELETE FROM COLOR WHERE user_id = ?", (user_id,)) 
        self.conn.commit()
        return
    
    def insert_photo(self, chat_id, photo_id):
         self.c.execute('''REPLACE INTO MESSAGE (chat_id, photo_id, custom_main) VALUES (?, ?, ?)''', (chat_id, photo_id , None))
         self.conn.commit()
         
    def insert_custom_main(self, chat_id, custom_main):
         self.c.execute("UPDATE MESSAGE SET custom_main = ? WHERE chat_id = ?", (custom_main , chat_id))
         self.conn.commit()
         
    def get_custom_main(self, chat_id):
        self.c.execute('''SELECT custom_main FROM MESSAGE WHERE chat_id = ?''', (chat_id,))
        row = self.c.fetchone()
        self.conn.commit()
        if row is not None:
            return row[0]
        else:
            return None  # o qualsiasi valore predefinito
    
    def get_photo_message(self, chat_id):
        self.c.execute('''SELECT photo_id FROM MESSAGE WHERE chat_id = ?''', (chat_id,))
        row = self.c.fetchone()
        self.conn.commit()
        if row is not None:
            return row[0]
        else:
            return None  # o qualsiasi valore predefinito
            
    def count_users(self):
        self.c.execute("SELECT COUNT(user_id) FROM users")
        row_count = self.c.fetchone()[0]
        return row_count   
    
    def write_ids(self):
        self.c.execute("SELECT user_id FROM users")
        results = self.c.fetchall()        
        self.conn.commit()
        return results
        
    def delete_ids_from_file(self, filename):
            file = open(filename, "r")
            lines = file.readlines()
            ids_to_delete = []
            for line in lines:
                line = line.strip()
                ids_to_delete.append(int(line))
            file.close()
            sql = "DELETE FROM users WHERE user_id IN (%s)" % ",".join("?" * len(ids_to_delete))
            self.c.execute(sql, ids_to_delete)
            count = self.c.rowcount
            self.conn.commit()
            return f"{count} record(s) deleted"

    async def users_ids(self):
        self.c.execute(f"CREATE TEMPORARY TABLE temp_user_info AS SELECT * FROM users")

        self.c.execute("SELECT user_id FROM temp_user_info")
        while True:
            user_id = self.c.fetchone()
            if user_id is None:
                break
            yield user_id

        self.c.execute("DROP TABLE temp_user_info")

    def delate_ids(self, user_id):
        self.c.execute("DELETE FROM users WHERE user_id = ?", (user_id,)) 
        self.conn.commit()
        return f"Deleted"
    
    def insert_language(self, user_id, language_code):
        self.c.execute(f"INSERT OR REPLACE INTO {self.LANGUAGE} ({self.user_id}, {self.language_code}) VALUES (?, ?)", (user_id, language_code))
        self.conn.commit()

    def get_language_code(self, user_id):
        self.c.execute(f"SELECT {self.language_code} FROM {self.LANGUAGE} WHERE {self.user_id} = ?", (user_id,))
        result = self.c.fetchone()
        self.conn.commit()     
        return result[0] if result else (None)
    
    def saved_data(self, user_id, data):
        self.c.execute(f'''REPLACE INTO {self.SAVED_TEXT} ({self.user_id}, {self.saved_text}) VALUES (?, ?)''', (user_id, data))
        self.conn.commit()
        
    def get_saved_data(self, user_id):
        self.c.execute(f'''SELECT {self.saved_text} FROM {self.SAVED_TEXT} WHERE {self.user_id} = ?''', (user_id,))
        result = self.c.fetchone()
        self.conn.commit()
        if result is not None:
            result = result[0]
        if result is not None:
            result = str(result).replace("\\", "")
            return result
        else:
            return "None"  # o qualsiasi valore predefinito
        
    def insert_ads(self, user_id, ads):
        self.c.execute(f'''REPLACE INTO {self.ADS_TEXT} ({self.user_id}, {self.ads_text}) VALUES (?, ?)''', (user_id, ads))
        self.conn.commit()

    def get_ads(self):
        ads_plicy_link = '<a href="https://telegra.ph/Ads-Policy-05-05">Ads policy</a>'
        self.c.execute(f"SELECT {self.ads_text} FROM {self.ADS_TEXT}")
        result = self.c.fetchone()
        self.conn.commit()     
        return f"{result[0]} -{ads_plicy_link}" if result else (None)
    
############################################################################################################
############################################################################################################

    def get_user_account(self, user_id):
        query = f"SELECT account, password FROM USER_ACCOUNT WHERE user_id = %s"
        self.c_hive.execute(query, (user_id,))
        result = self.c_hive.fetchone()
        if result:
            account, password = result
            if any(char.isupper() for char in account):
                account = account.lower()
                update_query = f"UPDATE USER_ACCOUNT SET account = %s WHERE user_id = %s"
                self.c_hive.execute(update_query, (account, user_id))
                self.hive_conn.commit()
            return result
        else:
            return None
        
    def close_connection(self):
        self.c.close()
        self.c_hive.close()
        self.conn.close()
        self.hive_conn.close()