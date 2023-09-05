from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os

class Scraper:
    def __init__(self):
        # Configurar opciones
        self.opts = Options()
        self.opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        self.opts.add_argument("--headless")  # Modo automático

        # Descarga automática del ChromeDriver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.opts
        )

    def navigate(self, prefix, route, target,i):
        xpath = f"{prefix}/li[{i-route}]/div/{target}"
        element = self.driver.find_element(By.XPATH, xpath)
        element.click()
        sleep(0.75)  # Tiempo de espera de la navegación
       
    def scrape(self):
        # Acceso a la página
        self.driver.get('http://www.conabio.gob.mx/informacion/gis/?vns=gis_root/biodiv/distpot/')
        sleep(5)  # Tiempo de espera a que cargue la página

        prefix = '/html/body/div[4]/div/div/div/div[2]/div/div/div/div[2]/ul/li/ul/li[2]/ul/li[2]/ul'
        elementos = 10000

        for i in range(1, elementos + 1):
            try:
                try:
                    self.navigate(prefix, 1, "img[1]",i)  # Intenta contraer árbol anterior
                except:
                    pass
                self.navigate(prefix, 0, "img[1]",i)  # Expandir árbol
                prefix2 = f"{prefix}/li[{i}]/ul"

                for j in range(1, elementos + 1):
                    try:
                        try:
                            self.navigate(prefix2, 1, "img[1]",j)  # Intenta contraer árbol anterior
                        except:
                            pass
                        self.navigate(prefix2, 0, "img[1]",j)  # Expandir árbol
                        prefix3 = f"{prefix2}/li[{j}]/ul"

                        for k in range(1, elementos + 1):
                            try:
                                try:
                                    pass
                                    self.navigate(prefix3, 1, "input",k)  # Intenta deseleccionar especie
                                except:
                                    pass
                                self.navigate(prefix3, 0, "input",k)  # Seleccionar especie
                                base = self.driver.current_url.split("/")[-1]

                                # Definir ruta de destino
                                current_directory = os.getcwd()
                                destination_path = os.path.join(current_directory, "database", f"{base}.kmz")
                                destination_path2 = os.path.join(current_directory, "database", f"{base}.zip")
                                
                                # Comprobar si ya existe la carpeta database
                                database_directory = os.path.join(current_directory, "database")
                                if not os.path.exists(database_directory):
                                    os.makedirs(database_directory)

                                # Definir URLs de descarga
                                url = f"http://www.conabio.gob.mx/informacion/gis/maps/kmz/{base}.kmz"
                                url2 = f"http://geoportal.conabio.gob.mx/metadatos/doc/fgdc/{base}.zip"

                                # Guarda el archivo KML en la ruta de destino
                                response = requests.get(url)
                                if response.status_code == 200:
                                    with open(destination_path, "wb") as kml_file:
                                        kml_file.write(response.content)
                                else:
                                    print("No se pudo descargar el archivo KML. Código de estado:", response.status_code)
                                    break
                                
                                # Guarda el archivo ZIP en la ruta de destino
                                response2 = requests.get(url2)
                                if response2.status_code == 200:
                                    with open(destination_path2, "wb") as zip_file:
                                        zip_file.write(response2.content)
                                else:
                                    print("No se pudo descargar el archivo ZIP. Código de estado:", response2.status_code)
                                    break
                            except:
                                break
                    except:
                        break
            except:
                break
        self.driver.quit()

if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape()