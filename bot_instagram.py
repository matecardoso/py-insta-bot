import os
import time
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from utils.login import login

def page_screenshot(driver):
    screenshot_path = "screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot tirado e salvo em: {screenshot_path}")

dotenv_path = find_dotenv()
if not dotenv_path:
    raise FileNotFoundError("Arquivo .env não encontrado")
load_dotenv(dotenv_path)

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Executa o Chrome em modo headless (sem interface gráfica, opcional)

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    if login(driver, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD):
        print("Login realizado com sucesso!")

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//span[@aria-label='Perfil']"))
            )
            print("Página inicial carregada com sucesso.")
        except Exception as e:
            print(f"Erro ao esperar o carregamento da página inicial: {e}")

        page_screenshot(driver)

    else:
        print("Falha no login.")

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    driver.quit()
