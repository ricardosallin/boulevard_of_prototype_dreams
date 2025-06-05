prompt='''
Perfeito! Um sonho sendo realizado :'-) Obrigado GPT!

Pensei em colocar rótulos em cima dos pontos com as coordenadas X,Y deles,, e também nas linhas com o comprimento delas. E à direita, um painel com a memória de cálculo sendo atualizada em tempo real.
'''

import tkinter as tk
from tkinter import Canvas
import math

class AreaCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Área - Fórmula do Agrimensor")

        # Layout geral
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        # Canvas à esquerda
        self.canvas = Canvas(self.main_frame, width=600, height=600, bg='white')
        self.canvas.pack(side="left", fill="both", expand=True)

        # Painel lateral à direita
        self.sidebar = tk.Frame(self.main_frame, width=200)
        self.sidebar.pack(side="right", fill="y")

        self.label_area = tk.Label(self.sidebar, text="Área: 0.0", font=("Arial", 14))
        self.label_area.pack(pady=10)

        self.memory_label = tk.Label(self.sidebar, text="Memória de cálculo:", font=("Arial", 12, "bold"))
        self.memory_label.pack()

        self.memory_text = tk.Text(self.sidebar, height=30, width=25, font=("Courier", 9))
        self.memory_text.pack(padx=5, pady=5, fill="y")

        # Dados e eventos
        self.points = []
        self.dragging_point = None

        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Button-3>", self.remove_point)
        self.canvas.bind("<B1-Motion>", self.drag_point)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)

    def add_point(self, event):
        for i, (x, y) in enumerate(self.points):
            if (event.x - x) ** 2 + (event.y - y) ** 2 < 100:
                self.dragging_point = i
                return
        self.points.append((event.x, event.y))
        self.draw()

    def remove_point(self, event):
        for i, (x, y) in enumerate(self.points):
            if (event.x - x) ** 2 + (event.y - y) ** 2 < 100:
                del self.points[i]
                self.draw()
                return

    def drag_point(self, event):
        if self.dragging_point is not None:
            self.points[self.dragging_point] = (event.x, event.y)
            self.draw()

    def stop_drag(self, event):
        self.dragging_point = None

    def draw(self):
        self.canvas.delete("all")
        self.memory_text.delete("1.0", tk.END)

        # Desenha polígono e rótulos
        n = len(self.points)
        if n > 1:
            self.canvas.create_polygon(self.points, outline="black", fill="#f0f0f0", width=2)

        for i, (x, y) in enumerate(self.points):
            r = 5
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="red")
            self.canvas.create_text(x, y - 12, text=f"({x},{y})", font=("Arial", 8), fill="blue")

            if i < n:
                x1, y1 = self.points[i]
                x2, y2 = self.points[(i + 1) % n]
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                dist = math.hypot(x2 - x1, y2 - y1)
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
            memory_log += f"{i:<4} {x1:<5} {y1:<5} {x2:<8} {y2:<8} {term:>8.2f}\n"

        memory_log += "-" * 60 + f"\nÁrea final = |Soma / 2| = {abs(area)/2:.2f}"

        return abs(area) / 2, memory_log

if __name__ == "__main__":
    root = tk.Tk()
    app = AreaCalculator(root)
    root.mainloop()
