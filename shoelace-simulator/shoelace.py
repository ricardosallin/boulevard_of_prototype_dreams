prompt='''
Olá GPT, tudo bem? Surgiu uma ideia de um projetinho aqui: um calculador de áreas com aquela "fórmula do agrimensor". A ideia é ter uma janela onde vc pode ir criando pontos ao clicar com o mouse, formando um polígono. Os pontos podem ser arrastados, e também excluídos se clicar neles com o botão direito. E o sistema calcula (usando essa fórmula) a área do polígono resultante. Pensei em fazer em Python, será q é complicado? Acho q nem precisa de DB neste caso, certo?
'''

import tkinter as tk
from tkinter import Canvas
import math

class AreaCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Área - Fórmula do Agrimensor")

        self.canvas = Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.points = []
        self.point_circles = []
        self.dragging_point = None

        self.label = tk.Label(root, text="Área: 0.0", font=("Arial", 14))
        self.label.pack()

        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Button-3>", self.remove_point)
        self.canvas.bind("<B1-Motion>", self.drag_point)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)

    def add_point(self, event):
        # Verifica se está clicando em ponto existente (para arrastar)
        for i, (x, y) in enumerate(self.points):
            if (event.x - x) ** 2 + (event.y - y) ** 2 < 100:
                self.dragging_point = i
                return

        # Adiciona novo ponto
        self.points.append((event.x, event.y))
        self.draw()

    def remove_point(self, event):
        # Remove ponto se clicado próximo
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
        self.point_circles = []

        # Desenha linhas do polígono
        if len(self.points) > 1:
            self.canvas.create_polygon(self.points, outline="black", fill="", width=2)

        # Desenha os pontos como círculos
        for x, y in self.points:
            r = 5
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="red")

        # Atualiza a área
        area = self.calculate_area()
        self.label.config(text=f"Área: {area:.2f}")

    def calculate_area(self):
        n = len(self.points)
        if n < 3:
            return 0.0

        area = 0.0
        for i in range(n):
            x1, y1 = self.points[i]
            x2, y2 = self.points[(i + 1) % n]
            area += (x1 * y2) - (x2 * y1)
        return abs(area) / 2

if __name__ == "__main__":
    root = tk.Tk()
    app = AreaCalculator(root)
    root.mainloop()
