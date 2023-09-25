import requests
from io import BytesIO
import zipfile
import xml.etree.ElementTree as ET  # Importar la librería para procesar XML

# Nombre de la especie actual
class descarga:
    def __init__(self, base):
        self.base = base
        self.limites_k = None
        self.origin = None
    
    def procesar(self):
        # Definir la URL de descarga
        url = f"http://geoportal.conabio.gob.mx/metadatos/doc/fgdc/{self.base}.zip"

        # Descargar el archivo ZIP en la memoria RAM
        response = requests.get(url)
        if response.status_code == 200:
            zip_data = BytesIO(response.content)

            # Extraer el contenido del archivo ZIP en memoria
            with zipfile.ZipFile(zip_data) as zip_file:
                # Lista de nombres de archivos en el ZIP
                file_names = zip_file.namelist()
                xml_file_name = f"{self.base}.xml"  

                if xml_file_name in file_names:
                    # Extraer el contenido del archivo XML
                    xml_data = zip_file.read(xml_file_name)

                    # Procesar el contenido XML
                    root = ET.fromstring(xml_data)
                    bounding_element = root.find(".//bounding")
                    if bounding_element is not None:
                        westbc = bounding_element.findtext("westbc")
                        eastbc = bounding_element.findtext("eastbc")
                        northbc = bounding_element.findtext("northbc")
                        southbc = bounding_element.findtext("southbc")
                        self.limites_k = [float(northbc),float(southbc),float(eastbc),float(westbc)]
                        
                    else:
                        print("Elemento 'bounding' no encontrado en el XML.")
                
                    # Acceder al valor de origin
                    origin_element = root.find(".//origin")
                    if origin_element is not None:
                        self.origin = origin_element.text
                    else:
                        print("Elemento 'origin' no encontrado en el XML.")
                else:
                    print(f"No se encontró el archivo XML ({xml_file_name}) en el ZIP.")
        else:
            print(f"No se pudo descargar el archivo {self.base}.zip desde la URL:", url)
