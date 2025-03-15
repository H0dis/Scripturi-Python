import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def apply_template(template_path, image_path, coords):
    # Incarca sablonul si imaginea
    template = cv2.imread(template_path)
    image = cv2.imread(image_path)

    if template is None or image is None:
        messagebox.showerror("Eroare", "Nu s-au putut incarca sablonul sau imaginea.")
        return None

    x, y, width, height = coords

    # Redimensioneaza imaginea la dimensiunea zonei albe
    resized_image = cv2.resize(image, (width, height))

    # Aplica imaginea pe sablon
    result = template.copy()
    result[y:y+height, x:x+width] = resized_image

    return result

def save_result(result):
    # Salveaza rezultatul intr-un fisier
    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        initialdir="C:/Users/Hodis Florin/Desktop/Work/4.Frontfinal"  # Schimba aceasta cale cu directorul dorit
    )
    if save_path:
        cv2.imwrite(save_path, result)
        messagebox.showinfo("Succes", f"Imaginea a fost salvata: {save_path}")

def load_template():
    # Incarca sablonul
    path = filedialog.askopenfilename(
        title="Selecteaza sablonul",
        filetypes=[("Imagini", "*.jpg;*.jpeg;*.png")],
        initialdir="C:/Users/Hodis Florin/Desktop/Work/2.Sabloane_fata"  # Schimba aceasta cale cu directorul dorit
    )
    return path

def load_image():
    # Incarca imaginea
    path = filedialog.askopenfilename(
        title="Selecteaza poza",
        filetypes=[("Imagini", "*.jpg;*.jpeg;*.png")],
        initialdir="C:/Users/Hodis Florin/Desktop/Work/1.Cover/1. Front"  # Schimba aceasta cale cu directorul dorit
    )
    return path

def detect_white_area(template_path, template_type, extinde=False):
    # Detecteaza zona alba in functie de tipul de sablon si daca este activata optiunea "extinde"
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        return None

    if not extinde:
        # Coordonatele default
        if template_type == "fata":
            coords = (157, 45, 498, 499)  # Coordonate pentru sablonul fata
        elif template_type == "spate":
            coords = (405, 45, 498, 499)  # Coordonate pentru sablonul spate
        else:
            return None
    else:
        # Coordonatele extinse
        if template_type == "fata":
            coords = (157, 45, 510, 505)  # Coordonate pentru sablonul fata extins
        elif template_type == "spate":
            coords = (395, 45, 510, 505)  # Coordonate pentru sablonul spate extins (extins spre stanga)
        else:
            return None
    return coords
# Actualizarea functiei principale pentru a include butonul "Extinde"
def main():
    root = tk.Tk()
    root.title("Editor Viniluri © Hodis Florin")

    template_path = None
    image_path = None
    result = None
    template_type = tk.StringVar(value="fata")
    extinde = tk.BooleanVar(value=False)  # Variabila pentru optiunea "extinde"

    def select_template():
        nonlocal template_path
        template_path = load_template()
        if template_path:
            template_img = Image.open(template_path)
            template_tk = ImageTk.PhotoImage(template_img)
            canvas_template.config(width=template_tk.width(), height=template_tk.height())
            canvas_template.create_image(0, 0, anchor=tk.NW, image=template_tk)
            canvas_template.image = template_tk

    def select_image():
        nonlocal image_path
        image_path = load_image()
        if template_path and image_path:
            preview_result()

    def preview_result():
        nonlocal result
        if not template_path or not image_path:
            messagebox.showerror("Eroare", "Selectati atat sablonul cat si poza.")
            return

        coords = detect_white_area(template_path, template_type.get(), extinde=extinde.get())
        if coords is None:
            messagebox.showerror("Eroare", "Nu s-a putut detecta zona alba.")
            return

        result = apply_template(template_path, image_path, coords)
        if result is not None:
            result_bgr = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            result_img = Image.fromarray(result_bgr)
            result_tk = ImageTk.PhotoImage(result_img)
            canvas_template.create_image(0, 0, anchor=tk.NW, image=result_tk)
            canvas_template.image = result_tk

    def save_image():
        if result is not None:
            save_result(result)
        else:
            messagebox.showerror("Eroare", "Nu exista nicio imagine de salvat.")

    # Interfata grafica
    canvas_template = tk.Canvas(root, width=600, height=400, bg="white")
    canvas_template.pack(side=tk.LEFT, padx=10, pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    btn_load_template = tk.Button(button_frame, text="Incarca Sablon", command=select_template)
    btn_load_template.pack(pady=5)

    btn_load_image = tk.Button(button_frame, text="Incarca Poza", command=select_image)
    btn_load_image.pack(pady=5)

    btn_save = tk.Button(button_frame, text="Salveaza", command=save_image)
    btn_save.pack(pady=5)

    # Optiuni pentru tipul de sablon
    tk.Radiobutton(button_frame, text="Fata", variable=template_type, value="fata").pack(pady=5)
    tk.Radiobutton(button_frame, text="Spate", variable=template_type, value="spate").pack(pady=5)

    # Optiune "Extinde"
    tk.Checkbutton(button_frame, text="Extinde", variable=extinde).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
