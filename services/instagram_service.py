import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

pycache_dir = os.path.join(os.getcwd(), 'pycache')
os.environ['PYTHONPYCACHEPREFIX'] = pycache_dir

if not os.path.exists(pycache_dir):
    os.makedirs(pycache_dir)

from utils.instagram_bot import InstagramBot

class InstagramService:
    def __init__(self):
        self.bot = InstagramBot()

    def login(self):
        self.bot.login()
    
    def get_followers(self, user_id, count=12):
        return self.bot.get_followers(user_id, count)
    
    def screenshot(self, filename="screenshot.png"):
        self.bot.page_screenshot(filename)
    
    def save_source(self, filename="page_source.html"):
        self.bot.save_page_source(filename)
    
    def close(self):
        self.bot.close()

if __name__ == "__main__":
    service = InstagramService()
    try:
        service.login()
        user_id = '1234302260'
        followers = service.get_followers(user_id)
        if followers:
            print("Seguidores:")
            print(followers)
        service.screenshot()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        service.close()
