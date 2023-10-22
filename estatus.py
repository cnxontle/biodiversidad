from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class StatusScraper:
    def __init__(self):
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        opts.add_argument("--disable-cache")
        opts.add_argument("--disable-application-cache")
        opts.add_argument("--disk-cache-size=0")
        opts.add_argument("--media-cache-size=0")
        opts.add_argument("--headless")
        self.driver = webdriver.Chrome(options=opts)
    
    def get_red_list_status(self, species_name):
        self.driver.get("https://www.iucnredlist.org/")
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
            return "No Encontrado"

    def close(self):
        self.driver.quit()


