import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
# import cv2
import numpy as np

class NESMapStitcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NES Map Stitcher")
        self.images = []  # [(filename, PIL image)]
        self.image_panels = []

        self.frame_top = tk.Frame(root)
        self.frame_top.pack(fill="x")

        self.btn_load = tk.Button(self.frame_top, text="Carregar Pasta de PNGs", command=self.load_folder)
        self.btn_load.pack(side="left", padx=5, pady=5)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = NESMapStitcherApp(root)
    root.mainloop()
