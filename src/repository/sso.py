
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

class SSOCONTROLLER:

    def __init__(self, selenium_url='http://selenium-relatorios:4444/wd/hub'):
        self.driver = webdriver.Remote(
            command_executor=selenium_url,
            options=Options()
        )

    def login(self, username, password):
        try:
            # Navega até a página de login
            self.driver.get("https://cisbaf.ssosamu.com:3001/SSONovaIguacu/Login.aspx")
            
            # Localiza os campos de login e senha
            input_login = self.get_element("Input User", '//*[@id="txtLogin"]', By.XPATH, 5)
            input_pass = self.get_element("Input Pass", '//*[@id="txtSenha"]', By.XPATH, 5)
            
            # Preenche os campos e realiza o envio
            input_login.send_keys(username)
            input_pass.send_keys(password, Keys.ENTER)
            
            # Aguarda a presença de um alerta e o aceita, caso exista
            try:
                wait = WebDriverWait(self.driver, timeout=5)
                alert = wait.until(EC.alert_is_present())
                alert.accept()
            except TimeoutException:
                print("Nenhum alerta encontrado após o login.")


            try:
                time.sleep(5)
                btn_update = self.get_element("Btn atualizar", '//*[@id="btnAtualizar"]', By.XPATH, 5)
                btn_update.click()
            except:
                pass
            # Aguarda o título da página mudar para verificar o sucesso do login
            try:
                wait = WebDriverWait(self.driver, timeout=5)
                wait.until(EC.title_contains("SSO - Sistema de Saúde OnLine"))
            except TimeoutException:
                raise Exception("Login não realizado com sucesso. Verifique as credenciais.")
            
        except Exception as e:
            raise Exception(f"Ocorreu um erro durante o login: {e}")
            
        
    def get_coockies(self):
        return self.driver.get_cookies()


    def get_element(self, name, search, type, time):
        try:
            return WebDriverWait(self.driver, time).until(
                EC.visibility_of_element_located((type, search))
            )
        except:
            raise Exception(f'Elemento {name} não encontrado')