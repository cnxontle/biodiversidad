from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class Servicio:
    # Inicialización del servicio en la clase (variable de clase)
    chrome_driver_service = Service(ChromeDriverManager().install())

    def __init__(self, headless=True):
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        opts.add_argument("--disable-cache")
        opts.add_argument("--disable-application-cache")
        opts.add_argument("--disk-cache-size=0")
        opts.add_argument("--media-cache-size=0")
        
        if headless:
            opts.add_argument("--headless")
        
        # Inicializa el driver utilizando el servicio de la clase
        self.driver = webdriver.Chrome(service=self.chrome_driver_service, options=opts)