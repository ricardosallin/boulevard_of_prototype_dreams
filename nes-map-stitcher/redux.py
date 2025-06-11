import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def reduzir_resolucao(imagem_path):
    try:
        img = Image.open(imagem_path)
        largura, altura = img.size

        nova_img = Image.new(img.mode, (largura // 2, altura // 2))
        pixels_originais = img.load()
        pixels_novos = nova_img.load()

        for y in range(0, altura, 2):
            for x in range(0, largura, 2):
                pixels_novos[x // 2, y // 2] = pixels_originais[x, y]

        nome, ext = os.path.splitext(imagem_path)
        destino_path = f"{nome}_reduzido{ext}"
        nova_img.save(destino_path)

        messagebox.showinfo("Sucesso", f"Imagem salva em:\n{destino_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao processar imagem:\n{str(e)}")

def selecionar_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("Imagens PNG", "*.png")])
    if caminho:
        reduzir_resolucao(caminho)

# Criar janela principal
janela = tk.Tk()
janela.title("Reduzir resolução de PNG 2x2")
janela.geometry("300x120")
janela.resizable(False, False)

# Botão
btn = tk.Button(janela, text="Selecionar imagem PNG", command=selecionar_arquivo)
btn.pack(expand=True, pady=30)

# Rodar interface
janela.mainloop()
