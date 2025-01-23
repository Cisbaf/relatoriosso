
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
from source.domain.coockie import Coockie


class SSOController:

    def __init__(self, user: str, password: str, selenium_url='http://selenium-relatorios:4444/wd/hub'):
        self.driver = webdriver.Remote(
            command_executor=selenium_url,
            options=Options()
        )
        self.__login__(user, password)

    def get_coockie(self):
        coockies = self.driver.get_cookies()
        self.driver.quit()
        auto_cookie_value = next((c['value'] for c in coockies if c['name'] == 'AutoCookie'), None)
        tr_acess_value = next((c['value'] for c in coockies if c['name'] == 'TrAcesso'), None)
        asp_session_value = next((c['value'] for c in coockies if c['name'] == 'ASP.NET_SessionId'), None)

        if auto_cookie_value is None or tr_acess_value is None or asp_session_value is None:
            raise ValueError("Um ou mais cookies obrigatórios estão ausentes.")

        return Coockie(
            asp_session_id=asp_session_value,
            tr_acess=tr_acess_value,
            auto_coockie=auto_cookie_value,
        )
        

    def __login__(self, username, password):
        try:
            # Navega até a página de login
            self.driver.get("https://cisbaf.ssosamu.com:3001/SSONovaIguacu/Login.aspx")
            
            # Localiza os campos de login e senha
            input_login = self._get_element_("Input User", '//*[@id="txtLogin"]', By.XPATH, 5)
            input_pass = self._get_element_("Input Pass", '//*[@id="txtSenha"]', By.XPATH, 5)
            
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
                btn_update = self._get_element_("Btn atualizar", '//*[@id="btnAtualizar"]', By.XPATH, 5)
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
            

    def _get_element_(self, name, search, type, time):
        try:
            return WebDriverWait(self.driver, time).until(
                EC.visibility_of_element_located((type, search))
            )
        except:
            raise Exception(f'Elemento {name} não encontrado')