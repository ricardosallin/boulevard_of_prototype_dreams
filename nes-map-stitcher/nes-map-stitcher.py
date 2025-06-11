import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import os
import numpy as np

class NESMapStitcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NES Map Stitcher")
        self.images = []  # [(filename, PIL image)]
        self.image_panels = []
        self.cuts = {}  # filename -> (left, top, right, bottom)

        self.frame_top = tk.Frame(root)
        self.frame_top.pack(fill="x")

        self.btn_load = tk.Button(self.frame_top, text="Carregar Pasta de PNGs", command=self.load_folder)
        self.btn_load.pack(side="left", padx=5, pady=5)

        self.btn_cut = tk.Button(self.frame_top, text="Cortar Bordas (por imagem)", command=self.set_crop)
        self.btn_cut.pack(side="left", padx=5, pady=5)

        self.btn_align = tk.Button(self.frame_top, text="Alinhar Pares", command=self.align_pair)
        self.btn_align.pack(side="left", padx=5, pady=5)

        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill="both", expand=True)

        self.scroll_x = tk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.pack(fill="x")
        self.canvas.configure(xscrollcommand=self.scroll_x.set)

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def load_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.clear_images()

        for fname in sorted(os.listdir(folder)):
            if fname.lower().endswith(".png"):
                full_path = os.path.join(folder, fname)
                img = Image.open(full_path)
                self.images.append((fname, img))

        self.show_previews()

    def clear_images(self):
        self.images.clear()
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.image_panels.clear()

    def show_previews(self):
        thumb_height = 120
        for i, (fname, img) in enumerate(self.images):
            ratio = thumb_height / img.height
            thumb = img.resize((int(img.width * ratio), thumb_height), Image.NEAREST)
            thumb_tk = ImageTk.PhotoImage(thumb)

            panel = tk.Label(self.inner_frame, image=thumb_tk, text=fname, compound="top")
            panel.image = thumb_tk
            panel.grid(row=0, column=i, padx=5, pady=5)
            self.image_panels.append(panel)

    def set_crop(self):
        if not self.images:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return

        filenames = [fname for fname, _ in self.images]
        fname = simpledialog.askstring("Corte", f"Nome do arquivo (exato):\n{filenames}")
        if not fname or fname not in filenames:
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            return

        left = simpledialog.askinteger("Corte Esquerda", "Pixels a cortar da esquerda:", initialvalue=0)
        top = simpledialog.askinteger("Corte Topo", "Pixels a cortar do topo:", initialvalue=0)
        right = simpledialog.askinteger("Corte Direita", "Pixels a cortar da direita:", initialvalue=0)
        bottom = simpledialog.askinteger("Corte Fundo", "Pixels a cortar do fundo:", initialvalue=0)
        self.cuts[fname] = (left, top, right, bottom)
        messagebox.showinfo("OK", f"Cortes salvos para {fname}.")

    def align_pair(self):
        if len(self.images) < 2:
            messagebox.showwarning("Aviso", "Pelo menos duas imagens são necessárias.")
            return

        filenames = [fname for fname, _ in self.images]
        fname1 = simpledialog.askstring("Alinhar", "Imagem 1 (nome):")
        fname2 = simpledialog.askstring("Alinhar", "Imagem 2 (nome):")

        img1 = next((img for f, img in self.images if f == fname1), None)
        img2 = next((img for f, img in self.images if f == fname2), None)

        if img1 is None or img2 is None:
            messagebox.showerror("Erro", "Imagens não encontradas.")
            return

        img1_c = self.apply_crop(fname1, img1)
        img2_c = self.apply_crop(fname2, img2)

        img1_cv = cv2.cvtColor(np.array(img1_c), cv2.COLOR_RGB2GRAY)
        img2_cv = cv2.cvtColor(np.array(img2_c), cv2.COLOR_RGB2GRAY)

        result = cv2.matchTemplate(img2_cv, img1_cv, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)

        offset_x, offset_y = max_loc
        messagebox.showinfo("Alinhamento", f"Melhor alinhamento encontrado: x={offset_x}, y={offset_y}")

    def apply_crop(self, fname, img):
        if fname in self.cuts:
            l, t, r, b = self.cuts[fname]
            return img.crop((l, t, img.width - r, img.height - b))
        return img

if __name__ == "__main__":
    root = tk.Tk()
    app = NESMapStitcherApp(root)
    root.mainloop()
