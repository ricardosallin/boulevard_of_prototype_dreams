import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def reduzir_resolucao(imagem_path, fator=2):
    try:
        img = Image.open(imagem_path)
        largura, altura = img.size

        nova_largura = largura // fator
        nova_altura = altura // fator
        nova_img = Image.new(img.mode, (nova_largura, nova_altura))

        pixels_originais = img.load()
        pixels_novos = nova_img.load()

        for y in range(0, altura, fator):
            for x in range(0, largura, fator):
                pixels_novos[x // fator, y // fator] = pixels_originais[x, y]

        nome, ext = os.path.splitext(imagem_path)
        destino_path = f"{nome}_reduzido_x{fator}{ext}"
        nova_img.save(destino_path)

        return destino_path
    except Exception as e:
        raise RuntimeError(f"Erro ao processar {imagem_path}:\n{e}")

def selecionar_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("Imagens PNG", "*.png")])
    if caminho:
        try:
            fator = int(entry_fator.get())
            destino = reduzir_resolucao(caminho, fator)
            messagebox.showinfo("Sucesso", f"Imagem salva em:\n{destino}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        fator = int(entry_fator.get())
        erros = []
        arquivos_processados = 0

        for nome_arquivo in os.listdir(pasta):
            if nome_arquivo.lower().endswith(".png"):
                caminho = os.path.join(pasta, nome_arquivo)
                try:
                    reduzir_resolucao(caminho, fator)
                    arquivos_processados += 1
                except Exception as e:
                    erros.append(str(e))

        if erros:
            messagebox.showwarning("Concluído com erros",
                                   f"{arquivos_processados} imagens processadas com sucesso.\n"
                                   f"{len(erros)} erros ocorreram.")
        else:
            messagebox.showinfo("Sucesso", f"Todas as imagens PNG da pasta foram reduzidas ({arquivos_processados}).")

# Criar janela principal
janela = tk.Tk()
janela.title("Reduzir resolução de PNG NxN")
janela.geometry("350x200")
janela.resizable(False, False)

# Widgets
label_fator = tk.Label(janela, text="Fator de redução (ex: 2, 3, 4):")
label_fator.pack(pady=(15, 0))

entry_fator = tk.Entry(janela, width=5)
entry_fator.insert(0, "2")
entry_fator.pack(pady=(0, 10))

btn_arquivo = tk.Button(janela, text="Processar imagem PNG", command=selecionar_arquivo)
btn_arquivo.pack(pady=5)

btn_pasta = tk.Button(janela, text="Processar pasta inteira", command=selecionar_pasta)
btn_pasta.pack(pady=5)

# Rodar interface
janela.mainloop()
