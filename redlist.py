from time import sleep
import navegador
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class StatusScraper:
    def __init__(self):
        servicio_driver = navegador.Servicio()
        self.driver = servicio_driver.driver
        self.driver.get("https://www.iucnredlist.org/search/list?query=&searchType=species")
        self.script = 'return document.evaluate(\'//*[@class="list-results__item"]//a[1]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.textContent;'
    
    def get_red_list_status(self, species_name):
        busqueda_de_especie = self.driver.find_element(By.XPATH, '//*[@id="nav-search"]/div/form/input')
        busqueda_de_especie.clear()
        sleep (0.5)
        texto_del_estatus = ""
        busqueda_de_especie.send_keys(species_name)
        sleep(2)
        try:
            estatus = self.driver.find_element(By.XPATH, '//*[@id="nav-search"]/div/div/section/ol/li/span[3]/strong')
            texto_del_estatus = estatus.text
            texto_del_estatus = texto_del_estatus.lower()
        except:
            sleep(2)
            try:
                estatus = self.driver.find_element(By.XPATH, '//*[@id="nav-search"]/div/div/section/ol/li/span[3]/strong')
                texto_del_estatus = estatus.text
                texto_del_estatus = texto_del_estatus.lower()
            except:
                texto_del_estatus = ""
        if texto_del_estatus == "lc":
            texto_del_estatus = "Least Concern"
        elif texto_del_estatus == "dd":
            texto_del_estatus = "Data Deficent"
        elif texto_del_estatus == "nt":
            texto_del_estatus = "Near Threatened"
        elif texto_del_estatus == "vu":
            texto_del_estatus = "Vulnerable"
        elif texto_del_estatus == "en":
            texto_del_estatus = "Endangered"
        elif texto_del_estatus == "cr":
            texto_del_estatus = "Critically Endangered"
        elif texto_del_estatus == "ew":
            texto_del_estatus = "Extinct in the Wild"
        elif texto_del_estatus == "ex":
            texto_del_estatus = "Extinct"
        elif texto_del_estatus == "ne":
            texto_del_estatus = "Not Evaluated"
        return texto_del_estatus

    def close(self):
        self.driver.quit()