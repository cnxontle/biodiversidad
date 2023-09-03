#Importar librerias
from time import sleep
from selenium import webdriver #pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
import requests
import os

#Configurar opciones
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
#opts.add_argument("--headless") # Modo automático

#Descarga automática del ChromeDriver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)
#Acceso a la pagina
driver.get('http://www.conabio.gob.mx/informacion/gis/?vns=gis_root/biodiv/distpot/')
sleep(5)#tiempo de espera a que cargue la pagina

prefijo = '/html/body/div[4]/div/div/div/div[2]/div/div/div/div[2]/ul/li/ul/li[2]/ul/li[2]/ul'
elementos = 10000

#Función para navegar por el arbol taxonomico
def navegacion (prefijo,rumbo,target):
    xpath = f"{prefijo}/li[{i-rumbo}]/div/{target}"
    anterior = driver.find_element(By.XPATH, xpath)
    anterior.click()
    sleep(0.5) #tiempo de espera de medio segundo

#Iterar sobre clases taxonomicas
for i in range(1, elementos + 1):
    try:
        try:
            navegacion(prefijo,1,"img[1]") #Intenta contraer arbol anterior
        except:
            pass
        navegacion(prefijo,0,"img[1]") #Expandir arbol
        prefijo2 = f"{prefijo}/li[{i}]/ul"
        
        for i in range(1, elementos + 1):
            try:
                try:
                    navegacion(prefijo2,1,"img[1]") #Intenta contraer arbol anterior
                except:
                    pass
                navegacion(prefijo2,0,"img[1]") #Expandir arbol
                prefijo3 = f"{prefijo2}/li[{i}]/ul"

                for i in range(1, elementos + 1):
                    try:
                        try:
                            pass
                            navegacion(prefijo3,1,"input") #Intenta Desseleccionar especie
                        except:
                            pass
                        navegacion(prefijo3,0,"input") #Seleccionar especie
                        base=driver.current_url.split("/")[-1]
                        
                        #Definir ruta de destino y url de descarga
                        current_directory = os.getcwd()
                        destination_path = os.path.join(current_directory, "database", f"{base}.kmz")
                        database_directory = os.path.join(current_directory, "database")
                        if not os.path.exists(database_directory):
                            os.makedirs(database_directory)
                        url = f"http://www.conabio.gob.mx/informacion/gis/maps/kmz/{base}.kmz"
                        
                        #Si hay respuesta guarda el contenido del archivo KML en la ruta de destino
                        response = requests.get(url)
                        if response.status_code == 200:
                            with open(destination_path, "wb") as kml_file:
                                kml_file.write(response.content)
                        else:
                            print("No se pudo descargar el archivo KML. Código de estado:", response.status_code)
                    except:
                        break
            except:
                break
    except:
        break

driver.quit()