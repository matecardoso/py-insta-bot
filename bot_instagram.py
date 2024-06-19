import os
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from utils.login import login

def page_screenshot(driver, filename="screenshot.png"):
    driver.save_screenshot(filename)
    print(f"Screenshot tirado e salvo em: {filename}")

def save_page_source(driver, filename="page_source.html"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print(f"Source da página salvo em: {filename}")

dotenv_path = find_dotenv()
if not dotenv_path:
    raise FileNotFoundError("Arquivo .env não encontrado")
load_dotenv(dotenv_path)

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
options.add_argument("--user-data-dir=./selenium_session")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://www.instagram.com/")
    print("Acessando a página do Instagram...")
    
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Profile']"))
        )
        print("Login já estava realizado.")
    except:
        print("Login não encontrado. Tentando logar...")
        try:
            if login(driver, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD):
                print("Login realizado com sucesso!")
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//span[text()='Profile']"))
                )
                print("Página inicial carregada com sucesso.")
            else:
                print("Falha no login.")
        except Exception as e:
            print(f"Ocorreu um erro durante o login: {e}")
            page_screenshot(driver, "login_error_screenshot.png")
            save_page_source(driver, "login_error_page_source.html")
            raise

    page_screenshot(driver)

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    driver.quit()
