## Objetivo
Recopilar información de la biodiversidad potencial y el estatus de las especies a partir de un polígono dado en el mapa

## Guía de Configuración

Asegúrate de tener las siguientes bibliotecas instaladas en tu entorno de Python. Puedes instalarlas utilizando pip:

```bash
pip install pandas
pip install openpyxl
pip install requests
pip install pymsgbox
pip install pillow
pip install selenium
pip install webdriver-manager
```
## Instrucciones

1. Ejecuta el archivo "scraper.py" para iniciar la búsqueda de especies.

2. Ingresa las coordenadas y el nivel de zoom del mapa. Antes de hacerlo, puedes enfocar el mapa en el área de tu interés para asegurarte de ingresar la posición correcta.

3. Después de establecer la posición inicial, dibuja el polígono que deseas evaluar y espera a que el programa termine su ejecución.

4. El "scraper" captura la pantalla del polígono inicial y verifica la imagen de cada especie en cada iteración para determinar su presencia. Si encuentra alguna especie en el polígono, se emitirá un sonido de notificación y se buscará el estado de esa especie en las listas de CITES, Red List y NOM-059.

5. Al finalizar la búsqueda, se le preguntará al usuario si desea verificar manualmente los resultados.

   - La opción "Omitir" no realizará ninguna verificación adicional.
   - La opción "Verificación Rápida" verificará solo aquellas especies con menos del 0.01% de probabilidad de ocurrencia.
   - La opción "Completa" verificará todas las probabilidades de ocurrencia, permitiendo al usuario determinar qué especies descartar de la lista final.

6. El proceso dura aproximadamente 3 horas, dependiendo del polígono evaluado. Los resultados se guardarán en el archivo "biodiversidad.xlsx" cuando el programa finalice su ejecución.
