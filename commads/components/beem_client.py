from beem import Steem, Hive
from beem.account import Account
from beem.blockchain import Blockchain
from beem.comment import Comment
from beem.community import Communities, Community
import requests
import json
from beem.nodelist import NodeList
from beem.exceptions import WrongMasterPasswordException, AccountExistsException
from beem.imageuploader import ImageUploader
from db import Database
from instance import bot
from config import admin_id
from db import Database
import sys
from logger_config import logger

class Blockchain:
    def __init__(self, mode='irreversible'):
        self.mode = mode
        self.steem_node = "https://api.moecki.online"
        self.hive_node = 'https://api.deathwing.me'
        self.nodelist = NodeList()
        #self.hive = Hive(node=self.nodelist.get_steem_nodes())
        self.stm = Steem(node=self.steem_node)
        self.hive = Hive(node=self.hive_node)
        self.community = Communities(blockchain_instance=self.stm)
        self.db = Database()
        self.print = print(sys.getdefaultencoding())
        self.wif = '5Jdhv6acxyCDx6e3QoFoyAAks6udkdv6jksp1ranAaoo7jib8cr'
        self.username = 'menny.trx'

    def hive_log(self, user_id, username='', wif=''):
        hive = Hive(key=[wif],node=self.hive_node)
        try:    
            account = Account(username, blockchain_instance=hive)  
        except Exception as ex:
            return "Account not exist 🚫"   
        self.db.insert_account_info(user_id, username, wif)
        hive.wallet.lock()
        return 'Account logged ✅'
    
    def hive_upload_image(self, file_path, user_id):
        hive = Hive(keys=[self.wif], node=self.hive_node)
        try:
            posting_key = hive.wallet.getPostingKeyForAccount(self.username)
        except Exception as ex:
            return "Key not exist 🚫"
        uploader = ImageUploader(blockchain_instance=hive)
        result = uploader.upload(file_path, self.username)
        return result['url']
    
    def steem_upload_image(self, file_path):
        username = "turbo.stm"
        wif = "5Kbqh238eCHFZgxvgWFB9SgBwTg5vkLLmB42BL1WhiNhwreTsJD"
        stm = Steem(keys=[wif], node=self.steem_node)
        try:
            posting_key = stm.wallet.getPostingKeyForAccount(username)
        except Exception as ex:
            return "Key not exist 🚫"
        uploader = ImageUploader(blockchain_instance=stm)
        result = uploader.upload(file_path, username)
        return result['url']
    
    def hive_public_post(self, user_id, title="", body="", tags="inleo leofinance", community='hive-167922'):
        result = self.db.get_account_info(user_id)
        hive = Hive(keys=[self.wif], node=self.hive_node)
        try:
            posting_key = hive.wallet.getPostingKeyForAccount(self.username)
        except Exception as ex:
            return "Key not exist 🚫"
        try:    
            account = Account(self.username, blockchain_instance=hive)  
        except Exception as ex:
            return "Account not exist 🚫"        
    
        result = hive.post(title=title, body=body, author=self.username, tags=tags, community=community)
        return f"Post '{title}' pubblicato con successo!"
    
    def steem_public_post(self, user_id, title="", body="", tags="italy steem steemit steemexclusive", community='hive-185836'):
        username = "turbo.stm"
        wif = "5Kbqh238eCHFZgxvgWFB9SgBwTg5vkLLmB42BL1WhiNhwreTsJD"
        stm = Steem(keys=[wif], node=self.steem_node)
        try:
            posting_key = stm.wallet.getPostingKeyForAccount(username)
        except Exception as ex:
            return "Key not exist 🚫"
        try:    
            account = Account(username, blockchain_instance=stm)  
        except Exception as ex:
            return "Account not exist 🚫"        
    
        result = stm.post(title=title, body=body, author=username, tags=tags, community=community)
        return f"Post '{title}' pubblicato con successo!"
    
    def get_hive_posts(self, username):
        headers = {'Content-Type': 'application/json'}
        data = {
            "jsonrpc": "2.0",
            "method": "condenser_api.get_discussions_by_blog",
            "params": [{"tag": username, "limit": 1}],
            "id": 1
        }
        response = requests.post(self.hive_node, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            data = response.json()
            link = data['result'][0]['url']
            url = f"https://peakd.com{link}"
            return url
        else:
            raise Exception(response.reason)
        
    def get_steem_posts(self, username):
        headers = {'Content-Type': 'application/json'}
        data = {
            "jsonrpc": "2.0",
            "method": "condenser_api.get_discussions_by_blog",
            "params": [{"tag": username, "limit": 1}],
            "id": 1
        }
        response = requests.post(self.steem_node, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            data = response.json()
            link = data['result'][0]['url']
            url = f"https://steemit.com{link}"
            return url
        else:
            raise Exception(response.reason)
        
    def get_steem_hive_price(self):
        url = 'https://imridd.eu.pythonanywhere.com/api/prices'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(response.reason)