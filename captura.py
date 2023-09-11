from PIL import ImageGrab, Image, ImageDraw

class PolygonCapture:
    def __init__(self, points):
        self.polygon_points = points
    
    def capture_polygon(self):
        # Capturar la pantalla completa
        screenshot = ImageGrab.grab()
        
        # Obtener las coordenadas extremas del polígono para definir el tamaño de la imagen
        min_x = min(p[0] for p in self.polygon_points)
        max_x = max(p[0] for p in self.polygon_points)
        min_y = min(p[1] for p in self.polygon_points)
        max_y = max(p[1] for p in self.polygon_points)
        
        # Crear una máscara con fondo transparente del mismo tamaño que la captura de pantalla
        mask = Image.new('L', screenshot.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.polygon(self.polygon_points, fill=255)
        
        # Aplicar la máscara a la captura de pantalla
        screenshot.putalpha(mask)
        
        # Recortar la imagen para que tenga la forma del polígono
        screenshot = screenshot.crop((min_x, min_y, max_x, max_y))
        
        # Retornar la imagen resultante
        return screenshot

# Uso de la clase
if __name__ == "__main__":
    polygon_capture = PolygonCapture()
    polygon_capture.capture_polygon()