import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.instagram_bot import InstagramBot

class InstagramService:
    def __init__(self):
        self.bot = InstagramBot()

    def login(self):
        self.bot.login()
    
    def get_followers(self, user_id):
        return self.bot.get_followers(user_id)
    
    def screenshot(self, filename="screenshot.png"):
        self.bot.page_screenshot(filename)
    
    def save_source(self, filename="page_source.html"):
        self.bot.save_page_source(filename)
    
    def close(self):
        self.bot.close()
