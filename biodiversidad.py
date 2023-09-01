from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
#opts.add_argument("--headless") # Headless Mode

# Descarga automática del ChromeDriver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)
driver.get('http://www.conabio.gob.mx/informacion/gis/?vns=gis_root/biodiv/distpot/')

sleep(3)
prefijo = '/html/body/div[4]/div/div/div/div[2]/div/div/div/div[2]/ul/li/ul/li[2]/ul/li[2]/ul'
elementos = 10000


titulos = driver.find_elements(By.XPATH, prefijo)
for titulo in titulos:
    print(titulo.text)


for i in range(1, elementos + 1):
    try:
        xpath = f"{prefijo}/li[{i}]/div/img[1]"
        elemento = driver.find_element(By.XPATH, xpath)
        elemento.click()
        sleep(0.5)
    except:
        break


sleep(3)