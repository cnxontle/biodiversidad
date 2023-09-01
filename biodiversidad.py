#Importar librerias
from time import sleep
from selenium import webdriver #pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager

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

#Seleccion de clases taxonomicas
titulos = driver.find_elements(By.XPATH, prefijo)
for titulo in titulos:
    print(titulo.text)

#Funcion para navegar por el arbol taxonomico
def navegacion (prefijo,rumbo):
    xpath = f"{prefijo}/li[{i-rumbo}]/div/img[1]"
    anterior = driver.find_element(By.XPATH, xpath)
    anterior.click()
    sleep(0.5)

#Iterar sobre clases taxonomicas
for i in range(1, elementos + 1):
    try:
        try:
            navegacion(prefijo,1) #intenta contraer arbol anterior
        except:
            pass
        navegacion(prefijo,0) #expandir arbol

        prefijo2 = f"{prefijo}/li[{i}]/ul"
        for i in range(1, elementos + 1):
            try:
                try:
                    navegacion(prefijo2,1) #intenta contraer arbol anterior
                except:
                    pass
                navegacion(prefijo2,0) #expandir arbol
            except:
                break
            


        
    except:
        break



driver.quit()