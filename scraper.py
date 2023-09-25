from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import poligono
import captura
import winsound
import pymsgbox
import pickle
from datos import descarga

# Crear un DataFrame vacío
column_names = ["ID", "Nivel_1", "Nivel_2", "Especie", "Referencias", "URL"]
df = pd.DataFrame(columns=column_names)
agregar_filas = []

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

# Función para navegar en el arbol 
def navigate(prefix, route, target,i):
    xpath = f"{prefix}/li[{i-route}]/div/{target}"
    element = driver.find_element(By.XPATH, xpath)
    element.click()
    if target == "input":
        xpath_temas = '//*[@id="footer-right"]/strong[1]'
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_temas)))
    sleep(0.3)  # Tiempo de espera de la navegacion en el arbol

# Evalua si los limites de dos mapas se superponen en su area
def traslape(limites_mapa1,limites_mapa2):
    superposicion= True
    if limites_mapa2[0] <= limites_mapa1[0]:
        if limites_mapa2[0] <= limites_mapa1[1]:
            superposicion = False
    else:
        if limites_mapa2[1]>= limites_mapa1[0]:
            superposicion = False
    if limites_mapa2[2] <= limites_mapa1[2]:
        if limites_mapa2[2] <= limites_mapa1[3]:
            superposicion = False
    else:
        if limites_mapa2[3]>= limites_mapa1[2]:
            superposicion = False
    return superposicion

# Acceso a la página
driver.maximize_window()
driver.get('http://www.conabio.gob.mx/informacion/gis/?vns=gis_root/biodiv/distpot/')
sleep(5)  # Tiempo de espera a que cargue la página
element = driver.find_element(By.XPATH, '//*[@id="ext-gen231"]')
element.click() # Cerrar mensaje de inicio 

# Parametros de navegación
prefix = '/html/body/div[4]/div/div/div/div[2]/div/div/div/div[2]/ul/li/ul/li[2]/ul/li[2]/ul'
elementos = 10000
change = 0
especie = ""
procesado = False
id_especie = 0

# Ajustar posicion y zoom inicial
valor = pymsgbox.prompt('Ingresa las coordenadas y el zoom separados por comas:',title='Ubicación de Inicio', default='Longitud,Latitud,Zoom')
zoom = valor.split(",")[2]
coordenada1 = valor.split(",")[1]
coordenada2 = valor.split(",")[0]
ajuste_coordenadas = f'map.panTo([{coordenada1}, {coordenada2}]);'
ajuste_zoom = f'map.setZoom({zoom});'
driver.execute_script(ajuste_zoom)
sleep(0.2)
driver.execute_script(ajuste_coordenadas)

# Obtener limites del mapa
script_obtener_limites = """
var bounds = map.getBounds();
var limites = [bounds.getNorth(), bounds.getSouth(), bounds.getEast(), bounds.getWest()];
return limites;
"""
limites_inicio = driver.execute_script(script_obtener_limites)

# Definir poligono del mapa
drawer = poligono.PolygonDrawer()
polygon_points = drawer.get_polygon_info()
sleep(1)

# Captura de pantalla inicial
capturas = captura.PolygonCapture(polygon_points)
screenshot_init = capturas.capture_polygon()

# Verificar si el archivo "limites.pkl" existe para leerlo o crear uno nuevo
if os.path.exists("limites.pkl"):
    modo_apertura = "rb+"
else:
    modo_apertura = "wb"
with open("limites.pkl", modo_apertura) as archivo:
    if modo_apertura == "rb+":
        try:
            limites = pickle.load(archivo)
        except EOFError:
            limites = {}
    else:
        limites = {}

# Busqueda de especies
    for i in range(1, elementos + 1):
        try:
            contenido_nivel1 = driver.find_element(By.XPATH, f"{prefix}/li[{i}]/div/a/span")
            cont_nivel1 = contenido_nivel1.text
            palabras_nivel1 = cont_nivel1.split()
            nivel1 = palabras_nivel1[0] 
            try:
                navigate(prefix, 1, "img[1]",i)  # Intenta contraer árbol anterior
            except:
                pass
            navigate(prefix, 0, "img[1]",i)  # Expandir árbol
            prefix2 = f"{prefix}/li[{i}]/ul"

            for j in range(1, elementos + 1):
                try:
                    contenido_nivel2 = driver.find_element(By.XPATH, f"{prefix2}/li[{j}]/div/a/span")
                    cont_nivel2 = contenido_nivel2.text
                    palabras_nivel2 = cont_nivel2.split()
                    nivel2 = palabras_nivel2[0] 
                    try:
                        navigate(prefix2, 1, "img[1]",j)  # Intenta contraer árbol anterior
                    except:
                        pass
                    navigate(prefix2, 0, "img[1]",j)  # Expandir árbol
                    prefix3 = f"{prefix2}/li[{j}]/ul"

                    for k in range(1, elementos + 1):
                        try:
                            contenido = driver.find_element(By.XPATH, f"{prefix3}/li[{k}]/div/a/span")
                            clave = contenido.text
                            palabras = clave.split()
                            especie_actual = " ".join(palabras[:2])
                            
                            if especie != especie_actual:
                                seleccionar = True
                                eval_traslape = True

                                # Si la clave se encuentra en el diccionario evaluar superposicion
                                if clave in limites:
                                    superposicion= traslape(limites_inicio,limites[clave])
                                    eval_traslape = False
                                    if superposicion == False:
                                        change += 1
                                        seleccionar = False

                                # Si la clave no se encuentra en el diccionario, seleccionar la especie
                                if seleccionar == True:
                                    try:
                                        navigate(prefix3, 1 + change, "input",k)  # Intenta deseleccionar especie
                                    except:
                                        pass
                                    navigate(prefix3, 0, "input",k)  # Seleccionar especie
                                    change = 0
                                    url = driver.current_url
                                    base = url.split("/")[-1]
    
                                    # Evaluar limites y Superposicion
                                    if eval_traslape == True:
                                        limites_k = []

                                        # Procesar archivo
                                        descargador = descarga(base)
                                        descargador.procesar()
                                        procesado = True

                                        # Acceder a los valores
                                        limites_k = descargador.limites_k
                                        origin = descargador.origin
                                        if limites_k == None:
                                            limites_k = driver.execute_script(script_obtener_limites)
                                        limites[clave] = limites_k
                                        superposicion= traslape(limites_inicio,limites_k)
                                        
                                if superposicion == True:
                                    # Ajustar el Mapa
                                    driver.execute_script(ajuste_zoom)
                                    sleep(0.5)
                                    driver.execute_script(ajuste_coordenadas)
                                    
                                    # Espera a que cargue el mapa
                                    try:
                                        for i in range(1, 9):
                                            xpath = '//*[@id="mview-panel"]/div[2]/div[1]/div[3]/div/img[' + str(i) + ']'
                                            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                                        sleep(0.1)
                                    except:
                                        pass
                                    # Verificar si hay presencia de la especie en el poligono para guardar la información
                                    screenshot_k = ""
                                    screenshot_k = capturas.capture_polygon()

                                    if screenshot_k != screenshot_init:
                                        winsound.Beep(500, 100)  # Reproducir un beep
                                        id_especie += 1
                                        especie = especie_actual

                                        if procesado == False:
                                            descargador = descarga(base)
                                            descargador.procesar()
                                            origin = descargador.origin
                                            nueva_fila = {
                                                "ID": id_especie,
                                                "Nivel_1": nivel1,
                                                "Nivel_2": nivel2,
                                                "Especie": especie_actual,
                                                "Referencias": origin,
                                                "URL": url,
                                            }
                                            agregar_filas.append(nueva_fila)
                            else:
                                change += 1            
                        except:
                            try:
                                navigate(prefix3, 1 + change, "input",k)  # Intenta deseleccionar especie
                            except:
                                pass
                            break
                except:
                    break
        except:
            break
    # Escribir los limites en el archivo limites.pkl
    if modo_apertura == "rb+":
        archivo.seek(0)
    pickle.dump(limites, archivo)

# Cerrar el Navegador
driver.quit()

# Guardar los resultados
df = pd.concat([df, pd.DataFrame(agregar_filas)], ignore_index=True)
nombre_archivo = "biodiversidad.csv"
df.to_csv(nombre_archivo, sep='\t', index=False, encoding="utf-16")