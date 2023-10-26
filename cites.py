from time import sleep
from selenium.webdriver.common.by import By
import navegador
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class CitesScraper:
    def __init__(self):
        servicio_driver = navegador.Servicio()
        self.driver = servicio_driver.driver
        self.driver.get("https://checklist.cites.org/#/es")

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        sleep(1)
        try:
            mensaje_inicio = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[1]/p[3]/a/span')
            mensaje_inicio.click()
        except:
            pass

    def get_cites_status(self, species_name):
        busqueda_de_especie = self.driver.find_element(By.XPATH, '//*[@id="scientific_name"]')
        busqueda_de_especie.clear()
        sleep(0.5)
        busqueda_de_especie.send_keys(species_name)
        busqueda_de_especie.send_keys(Keys.RETURN)
        sleep(1.5)
        try:
            estatus = self.driver.find_element(By.XPATH, '//*[@class="icons"]')
            texto_del_estatus = estatus.text
            texto_del_estatus = ", ".join(texto_del_estatus.split())
            return texto_del_estatus
        except:
            return ""

    def close(self):
        self.driver.quit()