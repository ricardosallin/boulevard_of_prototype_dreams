from PIL import Image, ImageDraw, ImageFont
import colorsys
import os

def rgb_to_hsl(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    return round(h * 360), round(s * 100), round(l * 100)

def rgb_to_hex(r, g, b):
    return f'#{r:02X}{g:02X}{b:02X}'

def extract_dominant_colors(image, max_colors):
    image = image.convert("RGB")
    result = image.quantize(colors=max_colors, method=2)
    palette = result.getpalette()
    color_counts = sorted(result.getcolors(), reverse=True)
    dominant_colors = [tuple(palette[i*3:i*3+3]) for i, _ in color_counts[:max_colors]]
    return dominant_colors

def extract_dominant_colors_safe(image, max_colors):
    image = image.convert("RGB")
    colors = image.getcolors(maxcolors=image.width * image.height)
    if not colors:
        raise ValueError("Too many colors in image for getcolors(). Try reducing image size or use quantization.")
    
    # Sort by count descending and extract RGB tuples
    sorted_colors = sorted(colors, reverse=True)
    dominant_colors = [rgb for count, rgb in sorted_colors[:max_colors]]
    return dominant_colors

def create_palette_image(colors, output_path, force_png=True):
    block_size = (60, 60)
    padding = 10
    font_size = 16
    width = 600
    height = (block_size[1] + padding) * len(colors)
    
    palette_img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(palette_img)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    for i, color in enumerate(colors):
        r, g, b = color
        h, s, l = rgb_to_hsl(r, g, b)
        hex_val = rgb_to_hex(r, g, b)

        y = i * (block_size[1] + padding)
        draw.rectangle([padding, y, padding + block_size[0], y + block_size[1]], fill=color, outline="black")
        text = f"RGB({r},{g},{b}) | HSL({h},{s}%,{l}%) | {hex_val}"
        draw.text((block_size[0] + 2 * padding, y + block_size[1]//3), text, fill="black", font=font)

    final_format = "PNG" if force_png else os.path.splitext(output_path)[-1][1:].upper()
    if force_png and not output_path.lower().endswith(".png"):
        output_path = os.path.splitext(output_path)[0] + ".png"

    palette_img.save(output_path, format=final_format)
    return output_path

def sort_colors(colors, method="hue"):
    if method == "hue":
        return sorted(colors, key=lambda rgb: colorsys.rgb_to_hls(*[v/255 for v in rgb])[0])
    elif method == "lightness":
        return sorted(colors, key=lambda rgb: colorsys.rgb_to_hls(*[v/255 for v in rgb])[1])
    else:
        return colors  # No sorting

# Atualizando função principal para usar o método seguro
def generate_color_palette(input_path, output_path, max_colors=20, force_png=True):
    image = Image.open(input_path)
    colors = extract_dominant_colors_safe(image, max_colors)
    return create_palette_image(colors, output_path, force_png)

def generate_color_palette(input_path, output_path=None, max_colors=20, force_png=True, order_by='hue'):
    image = Image.open(input_path)
    colors = extract_dominant_colors_safe(image, max_colors)
    colors = sort_colors(colors, order_by)

    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_ext = '.png' if force_png else ext
        output_path = f"{base}_colors{output_ext}"

    return create_palette_image(colors, output_path, force_png)

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def run_gui():
    def select_input_file():
        path = filedialog.askopenfilename(
            title="Selecione a imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif")],
        )
        if path:
            input_path_var.set(path)

    def generate_palette():
        input_path = input_path_var.get()
        max_colors = max_colors_var.get()
        force_png = force_png_var.get()
        order_by = order_by_var.get()

        if not input_path:
            messagebox.showerror("Erro", "Selecione uma imagem de entrada.")
            return

        try:
            output_path = generate_color_palette(
                input_path=input_path,
                output_path=None,
                max_colors=int(max_colors),
                force_png=bool(force_png),
                order_by=order_by
            )
            messagebox.showinfo("Sucesso", f"Paleta gerada com sucesso:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Erro ao gerar paleta", str(e))

    # GUI setup
    root = tk.Tk()
    root.title("Gerador de Paleta de Cores")

    input_path_var = tk.StringVar()
    max_colors_var = tk.IntVar(value=20)
    force_png_var = tk.BooleanVar(value=True)
    order_by_var = tk.StringVar(value="hue")

    tk.Label(root, text="Imagem de entrada:").grid(row=0, column=0, sticky="e")
    tk.Entry(root, textvariable=input_path_var, width=40).grid(row=0, column=1)
    tk.Button(root, text="Selecionar...", command=select_input_file).grid(row=0, column=2)

    tk.Label(root, text="Máx. de cores:").grid(row=1, column=0, sticky="e")
    tk.Spinbox(root, from_=1, to=256, textvariable=max_colors_var, width=5).grid(row=1, column=1, sticky="w")

    tk.Label(root, text="Ordenar por:").grid(row=2, column=0, sticky="e")
    ttk.Combobox(root, textvariable=order_by_var, values=["hue", "lightness", "none"], width=10).grid(row=2, column=1, sticky="w")

    tk.Checkbutton(root, text="Forçar saída PNG", variable=force_png_var).grid(row=3, column=1, sticky="w")

    tk.Button(root, text="Gerar Paleta", command=generate_palette).grid(row=4, column=1, pady=10)

    root.mainloop()

run_gui()
