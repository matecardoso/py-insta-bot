from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv, find_dotenv
import os

dotenv_path = find_dotenv()
if not dotenv_path:
    raise FileNotFoundError("Arquivo .env não encontrado")
load_dotenv(dotenv_path)

INSTAGRAM_BACKUP_CODES = os.getenv("INSTAGRAM_BACKUP_CODES").strip("[]").replace("\"", "").split(",")

def login(driver, username, password):
    try:
        print("Acessando a página de login do Instagram...")
        driver.get("https://www.instagram.com/accounts/login/")

        print("Esperando pelo campo de nome de usuário...")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        print("Campo de nome de usuário encontrado. Inserindo nome de usuário...")
        username_field.send_keys(username)

        print("Esperando pelo campo de senha...")
        password_field = driver.find_element(By.NAME, "password")
        print("Campo de senha encontrado. Inserindo senha...")
        password_field.send_keys(password)

        print("Clicando no botão de login...")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        print("Verificando se a autenticação de dois fatores é necessária...")
        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.find_element(By.NAME, "verificationCode") or d.find_element(By.XPATH, "//div[@role='dialog']")
            )
            print("Autenticação de dois fatores necessária. Usando código de reserva...")

            backup_code_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'código') or contains(., 'backup')]"))
            )

            for button in backup_code_buttons:
                if button.is_displayed() and button.is_enabled():
                    button.click()
                    break

            if INSTAGRAM_BACKUP_CODES:
                backup_code = INSTAGRAM_BACKUP_CODES.pop(0)
                backup_code_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "verificationCode"))
                )
                backup_code_field.send_keys(backup_code)

                confirm_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and (contains(text(), 'Confirmar') or contains(text(), 'Confirm'))]"))
                )
                confirm_button.click()

                update_env_file(INSTAGRAM_BACKUP_CODES)

            print("Login realizado com sucesso usando código de reserva!")
            return True

        except NoSuchElementException as e:
            print(f"Erro ao usar código de reserva: {e}")
            return False

    except Exception as e:
        print(f"Ocorreu um erro durante o login: {e}")
        return False

def update_env_file(codes):
    with open(dotenv_path, 'r') as file:
        data = file.readlines()

    with open(dotenv_path, 'w') as file:
        for line in data:
            if line.startswith('INSTAGRAM_BACKUP_CODES'):
                new_codes = 'INSTAGRAM_BACKUP_CODES=["' + '","'.join(codes) + '"]\n'
                file.write(new_codes)
            else:
                file.write(line)
