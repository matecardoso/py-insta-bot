from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from utils.login import login
from config.settings import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, INSTAGRAM_BACKUP_CODES
import requests
import os

class InstagramBot:
    def __init__(self):
        self.setup_driver()
    
    def setup_driver(self):
        session_path = os.path.join(os.getcwd(), "browser_data", "selenium_session")
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_argument(f"--user-data-dir={session_path}")
        
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
    
    def login(self):
        self.driver.get("https://www.instagram.com/")
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Profile']"))
            )
        except:
            if login(self.driver, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, INSTAGRAM_BACKUP_CODES):
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//span[text()='Profile']"))
                )
    
    def get_cookies(self):
        cookies = self.driver.get_cookies()
        session_cookies = {cookie['name']: cookie['value'] for cookie in cookies}
        return session_cookies
    
    def get_user_agent(self):
        return self.driver.execute_script("return navigator.userAgent;")
    
    def get_headers(self):
        headers = {
            'User-Agent': self.get_user_agent(),
            'Referer': 'https://www.instagram.com/',
            'X-CSRFToken': self.driver.get_cookie('csrftoken')['value'],
            'X-IG-App-ID': '936619743392459',
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        }
        return headers
    
    def get_followers(self, user_id):
        cookies = self.get_cookies()
        headers = self.get_headers()
        followers = []
        max_id = ''
        
        while True:
            url = f'https://www.instagram.com/api/v1/friendships/{user_id}/followers/?count=100&search_surface=follow_list_page&max_id={max_id}'
            response = requests.get(url, headers=headers, cookies=cookies)
            
            if response.status_code != 200:
                print(f"Falha ao obter seguidores: {response.status_code}")
                print(response.text)
                return None
            
            data = response.json()
            followers.extend(data['users'])
            if 'next_max_id' in data and data['next_max_id']:
                max_id = data['next_max_id']
            else:
                break
        
        return followers
    
    def get_following(self, user_id):
        cookies = self.get_cookies()
        headers = self.get_headers()
        following = []
        max_id = ''
        
        while True:
            url = f'https://www.instagram.com/api/v1/friendships/{user_id}/following/?count=100&search_surface=follow_list_page&max_id={max_id}'
            response = requests.get(url, headers=headers, cookies=cookies)
            
            if response.status_code != 200:
                print(f"Falha ao obter quem você segue: {response.status_code}")
                print(response.text)
                return None
            
            data = response.json()
            following.extend(data['users'])
            if 'next_max_id' in data and data['next_max_id']:
                max_id = data['next_max_id']
            else:
                break
        
        return following
    
    def close(self):
        self.driver.quit()
    
    def page_screenshot(self, filename="screenshot.png"):
        self.driver.save_screenshot(filename)
    
    def save_page_source(self, filename="page_source.html"):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.driver.page_source)
