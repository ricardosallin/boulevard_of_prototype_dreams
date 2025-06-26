gpt_suggestions='''
Se quiser, posso:
- Adicionar zoom e pan (arrastar o canvas).
- Permitir salvar o polígono em .txt ou .png.
- Adicionar grid no fundo para referência visual.
É só dizer — seguimos nessa jornada! 😄
'''

prompt='''
Gosto dessas três ideias! O grid é opcional (usuário ativa ou não) e segue o zoom sendo aplicado, mudando conforme necessidade (de 100 em 100, de 10 em 10, de 1 em 1).

O zoom vai ser pela rodinha do mouse?

E o salvar pode ser em jpg, txt ou Json tb, pra incluir a memória de cálculo 
'''

# Etapa 1: Adicionar zoom com scroll do mouse
# Etapa 2: Checkbox para mostrar/ocultar grid adaptável ao zoom
# Etapa 3: Botões para exportar em .txt, .json e .png

from tkinter import Tk, Frame, Canvas, Label, Text, Button, Checkbutton, BooleanVar, filedialog
import tkinter as tk
import math
import json
from PIL import Image, ImageDraw

class AreaCalculatorZoom:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Área com Zoom e Exportação")

        # Layout
        self.main_frame = Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.canvas = Canvas(self.main_frame, width=600, height=600, bg='white')
        self.canvas.pack(side="left", fill="both", expand=True)

        self.sidebar = Frame(self.main_frame, width=200)
        self.sidebar.pack(side="right", fill="y")

        self.label_area = Label(self.sidebar, text="Área: 0.0", font=("Arial", 14))
        self.label_area.pack(pady=10)

        self.memory_label = Label(self.sidebar, text="Memória de cálculo:", font=("Arial", 12, "bold"))
        self.memory_label.pack()

        self.memory_text = Text(self.sidebar, height=20, width=25, font=("Courier", 9))
        self.memory_text.pack(padx=5, pady=5, fill="y")

        # Opção de grid
        self.show_grid = BooleanVar(value=True)
        self.grid_check = Checkbutton(self.sidebar, text="Mostrar Grid", variable=self.show_grid, command=self.draw)
        self.grid_check.pack()

        # Botões de exportação
        Button(self.sidebar, text="Exportar como TXT", command=self.export_txt).pack(pady=2)
        Button(self.sidebar, text="Exportar como JSON", command=self.export_json).pack(pady=2)
        Button(self.sidebar, text="Exportar como PNG", command=self.export_png).pack(pady=2)

        # Dados
        self.points = []
        self.dragging_point = None
        self.zoom = 1.0
        self.offset = (0, 0)

        # Eventos
        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Button-3>", self.remove_point)
        self.canvas.bind("<B1-Motion>", self.drag_point)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<MouseWheel>", self.zoom_handler)  # Windows/Linux
        self.canvas.bind("<Button-4>", lambda e: self.zoom_handler(e, 1))  # Mac scroll up
        self.canvas.bind("<Button-5>", lambda e: self.zoom_handler(e, -1))  # Mac scroll down

    def to_canvas_coords(self, x, y):
        return x * self.zoom + self.offset[0], y * self.zoom + self.offset[1]

    def from_canvas_coords(self, x, y):
        return (x - self.offset[0]) / self.zoom, (y - self.offset[1]) / self.zoom

    def add_point(self, event):
        x, y = self.from_canvas_coords(event.x, event.y)
        for i, (px, py) in enumerate(self.points):
            cx, cy = self.to_canvas_coords(px, py)
            if (event.x - cx) ** 2 + (event.y - cy) ** 2 < 100:
                self.dragging_point = i
                return
        self.points.append((x, y))
        self.draw()

    def remove_point(self, event):
        x, y = self.from_canvas_coords(event.x, event.y)
        for i, (px, py) in enumerate(self.points):
            cx, cy = self.to_canvas_coords(px, py)
            if (event.x - cx) ** 2 + (event.y - cy) ** 2 < 100:
                del self.points[i]
                self.draw()
                return

    def drag_point(self, event):
        if self.dragging_point is not None:
            x, y = self.from_canvas_coords(event.x, event.y)
            self.points[self.dragging_point] = (x, y)
            self.draw()

    def stop_drag(self, event):
        self.dragging_point = None

    def zoom_handler(self, event, direction=None):
        scale = 1.1 if (event.delta > 0 if direction is None else direction > 0) else 0.9
        self.zoom *= scale
        self.draw()

    def draw_grid(self):
        step = 100
        if self.zoom > 3:
            step = 1
        elif self.zoom > 1.5:
            step = 10

        width = int(self.canvas.winfo_width())
        height = int(self.canvas.winfo_height())
        for x in range(0, int(width), int(step * self.zoom)):
            self.canvas.create_line(x, 0, x, height, fill="#eee")
        for y in range(0, int(height), int(step * self.zoom)):
            self.canvas.create_line(0, y, width, y, fill="#eee")

    def draw(self):
        self.canvas.delete("all")
        self.memory_text.delete("1.0", tk.END)

        if self.show_grid.get():
            self.draw_grid()

        n = len(self.points)
        screen_points = [self.to_canvas_coords(x, y) for (x, y) in self.points]

        if n > 1:
            self.canvas.create_polygon(screen_points, outline="black", fill="#f0f0f0", width=2)

        for i, (x, y) in enumerate(screen_points):
            r = 4
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="red")
            px, py = self.points[i]
            self.canvas.create_text(x, y - 10, text=f"({px:.1f},{py:.1f})", font=("Arial", 8), fill="blue")

            if n > 1:
                x1, y1 = screen_points[i]
                x2, y2 = screen_points[(i + 1) % n]
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                dist = math.hypot(self.points[(i + 1) % n][0] - self.points[i][0],
                                  self.points[(i + 1) % n][1] - self.points[i][1])
                self.canvas.create_text(mid_x, mid_y, text=f"{dist:.1f}", font=("Arial", 8), fill="green")

        area, memory = self.calculate_area()
        self.label_area.config(text=f"Área: {area:.2f}")
        self.memory_text.insert(tk.END, memory)

    def calculate_area(self):
        n = len(self.points)
        if n < 3:
            return 0.0, "Polígono incompleto (menos de 3 pontos)."

        area = 0.0
        memory_log = "i    x_i   y_i   x_{i+1} y_{i+1}   x_i*y_{i+1} - x_{i+1}*y_i\n"
        memory_log += "-" * 60 + "\n"

        for i in range(n):
            x1, y1 = self.points[i]
            x2, y2 = self.points[(i + 1) % n]
            term = x1 * y2 - x2 * y1
            area += term
            memory_log += f"{i:<4} {x1:<5.1f} {y1:<5.1f} {x2:<8.1f} {y2:<8.1f} {term:>8.2f}\n"

        memory_log += "-" * 60 + f"\nÁrea final = |Soma / 2| = {abs(area)/2:.2f}"
        return abs(area) / 2, memory_log

    def export_txt(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if not file_path: return
        area, memory = self.calculate_area()
        with open(file_path, "w") as f:
            f.write("Coordenadas dos pontos:\n")
            for x, y in self.points:
                f.write(f"({x}, {y})\n")
            f.write(f"\nÁrea: {area:.2f}\n\nMemória de cálculo:\n{memory}")

    def export_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json")
        if not file_path: return
        area, memory = self.calculate_area()
        data = {
            "pontos": self.points,
            "area": area,
            "memoria_calculo": memory
        }
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def export_png(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if not file_path: return

        # Renderiza imagem com Pillow
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        screen_points = [self.to_canvas_coords(x, y) for (x, y) in self.points]
        if len(screen_points) > 2:
            draw.polygon(screen_points, outline="black", fill="#f0f0f0")

        for x, y in screen_points:
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

        image.save(file_path)


if __name__ == "__main__":
    root = Tk()
    app = AreaCalculatorZoom(root)
    root.mainloop()
