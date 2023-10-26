from time import sleep
import navegador
from selenium.webdriver.common.by import By

class StatusScraper:
    def __init__(self):
        servicio_driver = navegador.Servicio()
        self.driver = servicio_driver.driver
        self.driver.get("https://www.iucnredlist.org/")

    def get_red_list_status(self, species_name):
        busqueda_de_especie = self.driver.find_element(By.XPATH, '//*[@id="nav-search"]/div/form/input')
        busqueda_de_especie.clear()
        sleep(0.5)
        busqueda_de_especie.send_keys(species_name)
        sleep(1.5)
        try:
            estatus = self.driver.find_element(By.XPATH, '//*[@id="nav-search"]/div/div/section/ol/li/span[3]')
            texto_del_estatus = estatus.text
            if texto_del_estatus == "<LC>":
                texto_del_estatus = "Least Concern"
            elif texto_del_estatus == "<DD>":
                texto_del_estatus = "Data Deficent"
            elif texto_del_estatus == "<NT>":
                texto_del_estatus = "Near Threatened"
            elif texto_del_estatus == "<VU>":
                texto_del_estatus = "Vulnerable"
            elif texto_del_estatus == "<EN>":
                texto_del_estatus = "Endangered"
            elif texto_del_estatus == "<CR>":
                texto_del_estatus = "Critically Endangered"
            elif texto_del_estatus == "<EW>":
                texto_del_estatus = "Extinct in the Wild"
            elif texto_del_estatus == "<EX>":
                texto_del_estatus = "Extinct"
            elif texto_del_estatus == "<NE>":
                texto_del_estatus = "Not Evaluated"
            return texto_del_estatus
        except:
            return ""

    def close(self):
        self.driver.quit()