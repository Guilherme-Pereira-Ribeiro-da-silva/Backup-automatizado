from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class backup:
    def __init__(self):
        self.driver = webdriver.Chrome('E:\\backup-automatizado\\venv\\src\\arquivos\\chromedriver.exe')

    def AbrirBrowser(self,url):
        self.driver.get(url)

    def LimparInput(self,id):
        self.driver.find_element(By.ID, id).clear()

    def InserirInfoElemento(self,id,conteudo):
        elemento = self.driver.find_element(By.ID,id)
        elemento.send_keys(conteudo)

    def ClicarNoElemento(self,id):
        self.driver.find_element(By.ID,id).click()

    def ClicarElementoPorXPath(self,xpath):
        self.driver.find_element(By.XPATH,xpath).click()

    def TrocarDePagina(self,index):
        self.driver.switch_to.window(self.driver.window_handles[index])

    def GetConteudoElemento(self,xpath):
        return self.driver.find_element(By.XPATH,xpath).text

    def FecharTelaAtual(self):
        self.driver.close()

    def DuploCliqueElemento(self,id):
        action = ActionChains(self.driver)
        action.double_click(self.driver.find_element(By.ID,id)).perform()

    def DuploCliqueElementoXPath(self, xpath):
        action = ActionChains(self.driver)
        action.double_click(self.driver.find_element(By.XPATH, xpath)).perform()

    def CliqueDireitoElemento(self,id):
        action = ActionChains(self.driver)
        action.context_click(self.driver.find_element(By.ID,id)).perform()

    def CliqueDireitoElementoXPath(self,xpath):
        action = ActionChains(self.driver)
        action.context_click(self.driver.find_element(By.XPATH,xpath)).perform()

    def EsperarElementoSerClicavel(self,id):
        WebDriverWait(self.driver,3600).until(EC.element_to_be_clickable((By.ID,id)))

    def EsperarElementoSerClicavelXPath(self,XPath):
        WebDriverWait(self.driver,3600).until(EC.element_to_be_clickable((By.XPATH,XPath)))

    def FecharBrowser(self):
        self.driver.close()