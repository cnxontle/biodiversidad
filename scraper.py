from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import poligono
import captura
import winsound
import pymsgbox


# Configurar opciones
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
opts.add_argument("--disable-cache")  # Deshabilitar la caché
opts.add_argument("--disable-application-cache")  # Deshabilitar la caché de aplicaciones
opts.add_argument("--disk-cache-size=0")  # Establecer el tamaño de la caché en 0
opts.add_argument("--media-cache-size=0")  # Establecer el tamaño de la caché de medios en 0

# Descarga automática del ChromeDriver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)
        
def navigate(prefix, route, target,i):
    xpath = f"{prefix}/li[{i-route}]/div/{target}"
    element = driver.find_element(By.XPATH, xpath)
    element.click()
    sleep(0.3)  # Tiempo de espera de la navegación
       
# Acceso a la página
driver.maximize_window()
driver.get('http://www.conabio.gob.mx/informacion/gis/?vns=gis_root/biodiv/distpot/')
sleep(5)  # Tiempo de espera a que cargue la página
        
# Parametros de navegación
prefix = '/html/body/div[4]/div/div/div/div[2]/div/div/div/div[2]/ul/li/ul/li[2]/ul/li[2]/ul'
elementos = 10000

# Cerrar mensaje de inicio 
element = driver.find_element(By.XPATH, '//*[@id="ext-gen231"]')
element.click()

# definir valores de inicio
valor = pymsgbox.prompt('Ingresa las coordenadas y el zoom separados por comas:',title='Ubicación de Inicio', default='Longitud,Latitud,Zoom')

# Scripts para ajustar posicion y zoom
ajuste_coordenadas = f'map.panTo([{valor.split(",")[1]}, {valor.split(",")[0]}]);'
ajuste_zoom = f'map.setZoom({valor.split(",")[2]});'

# Scripts para ajustar posicion y zoom
driver.execute_script(ajuste_zoom)
sleep(0.2)
driver.execute_script(ajuste_coordenadas)

# Obtener limites del cuadro inicial
script_obtener_limites = """
var bounds = map.getBounds();
var limites = [bounds.getNorth(), bounds.getSouth(), bounds.getEast(), bounds.getWest()];
return limites;
"""
# Ejecuta el script y obtén los límites del mapa
limites_inicio = driver.execute_script(script_obtener_limites)

# Definir poligono del mapa
drawer = poligono.PolygonDrawer()
polygon_points = drawer.get_polygon_info()
sleep(1)

# Captura inicial
capturas = captura.PolygonCapture(polygon_points)
screenshot_init = capturas.capture_polygon()

# Busqueda de especies
for i in range(1, elementos + 1):
    try:
        try:
            navigate(prefix, 1, "img[1]",i)  # Intenta contraer árbol anterior
        except:
            pass
        navigate(prefix, 0, "img[1]",i)  # Expandir árbol
        prefix2 = f"{prefix}/li[{i}]/ul"

        for j in range(1, elementos + 1):
            try:
                try:
                    navigate(prefix2, 1, "img[1]",j)  # Intenta contraer árbol anterior
                except:
                    pass
                navigate(prefix2, 0, "img[1]",j)  # Expandir árbol
                prefix3 = f"{prefix2}/li[{j}]/ul"

                for k in range(1, elementos + 1):
                    try:
                        try:
                            pass
                            navigate(prefix3, 1, "input",k)  # Intenta deseleccionar especie
                        except:
                            pass
                        navigate(prefix3, 0, "input",k)  # Seleccionar especie
                        base = driver.current_url.split("/")[-1]

                        # Evaluar limites y Superposicion
                        limites_k = []
                        limites_k = driver.execute_script(script_obtener_limites)

                        superposicion= True

                        if limites_k[0] <= limites_inicio[0]:
                            if limites_k[0] <= limites_inicio[1]:
                                superposicion = False
                        else:
                            if limites_k[1]>= limites_inicio[0]:
                                superposicion = False
                           
                        if limites_k[2] <= limites_inicio[2]:
                            if limites_k[2] <= limites_inicio[3]:
                                superposicion = False
                        else:
                            if limites_k[3]>= limites_inicio[2]:
                                superposicion = False
                        
                        if superposicion == True:
                            # Ajustar el Mapa
                            driver.execute_script(ajuste_zoom)
                            sleep(0.5)
                            driver.execute_script(ajuste_coordenadas)
                            
                            # Espera a que cargue el layer
                            
                            WebDriverWait(driver, 10).until(
                                EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="mview-panel"]/div[2]/div[1]/div[3]/div/img[9]')))
                            
                            # Verificar si hay presencia de la especie en el poligono para guardar la información
                            screenshot_k = ""
                            screenshot_k = capturas.capture_polygon()

                            if screenshot_k != screenshot_init:
                                winsound.Beep(500, 100)  # Reproducir un beep estándar
                                
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
                                sleep(0.5)
                    except:
                        break
            except:
                break
    except:
        break
driver.quit()