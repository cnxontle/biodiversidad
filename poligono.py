import tkinter as tk

#Esta clase se usa para definir el poligono del mapa que queremos evaluar
class PolygonDrawer:
    def __init__(self):
        self.root = tk.Tk()
        
        self.root.attributes("-alpha", 0.1)  # Configura la transparencia (0.0 - 1.0)
        self.root.wait_visibility()
        self.canvas = tk.Canvas(self.root, width=850, height=650)
        self.ventana_ancho = 850
        self.ventana_alto = 650
        
        # Obtiene el tamaño de la pantalla
        self.pantalla_ancho = self.root.winfo_screenwidth()
        self.pantalla_alto = self.root.winfo_screenheight()

        # Calcula las coordenadas para centrar la ventana
        self.x = ((self.pantalla_ancho - self.ventana_ancho) // 2)+35
        self.y = (self.pantalla_alto - self.ventana_alto) // 2

        # Configura la geometría de la ventana y centra la ventana
        self. root.geometry(f"{self.ventana_ancho}x{self.ventana_alto}+{self.x}+{self.y}")
        self.root.overrideredirect(True)
        self.canvas.pack()
        self.points = []
        self.polygon = None
        self.drawing = False

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.complete_polygon)
        self.root.mainloop()

    def start_drawing(self, event):
        if not self.drawing:
            self.points = [(event.x, event.y)]
            self.drawing = True

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            self.points.append((x, y))
            self.canvas.create_line(self.points[-2], self.points[-1])

    def complete_polygon(self, event):
        if self.drawing:
            self.drawing = False
            if len(self.points) >= 3:
                self.points.append(self.points[0])  # Cierra el poligono
                self.polygon = self.canvas.create_polygon(self.points, outline='black', fill='', width=4)

                # Obtiene la posición de la ventana en el monitor
                root_x = self.root.winfo_x()
                root_y = self.root.winfo_y()

                # Ajusta las coordenadas de los puntos según la posición de la ventana
                adjusted_points = [(x + root_x, y + root_y) for x, y in self.points]

                # Convierte los puntos ajustados en una lista de tuplas
                polygon_info = list(map(tuple, adjusted_points))

                # Guarda el polígono y su posición
                self.polygon_info = polygon_info
                self.root.quit()
                
    def get_polygon_info(self):
        return self.polygon_info
    
    def destroy(self):
        self.root.destroy()

if __name__ == "__main__":

    PolygonDrawer()
    
