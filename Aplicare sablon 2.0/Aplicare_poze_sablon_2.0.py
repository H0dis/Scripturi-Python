import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

def apply_template(template_path, image_path, coords):
    template = cv2.imread(template_path)
    image = cv2.imread(image_path)

    if template is None or image is None:
        messagebox.showerror("Eroare", "Nu s-au putut incarca sablonul sau imaginea.")
        return None

    x, y, width, height = coords
    resized_image = cv2.resize(image, (width, height))
    result = template.copy()
    result[y:y+height, x:x+width] = resized_image

    return result

def resize_logo(logo, target_size=81):
    h, w, _ = logo.shape
    scale = target_size / max(h, w)
    new_size = (int(w * scale), int(h * scale))
    return cv2.resize(logo, new_size, interpolation=cv2.INTER_AREA)

def apply_logo(image, logo, position):
    h, w, _ = image.shape
    lh, lw, _ = logo.shape
    x_offset, y_offset = position
    x_offset = min(max(0, x_offset), w - lw)
    y_offset = min(max(0, y_offset), h - lh)

    if logo.shape[2] == 4:
        logo_alpha = logo[:, :, 3] / 255.0
        logo_rgb = logo[:, :, :3]
        for c in range(3):
            image[y_offset:y_offset+lh, x_offset:x_offset+lw, c] = (
                (1 - logo_alpha) * image[y_offset:y_offset+lh, x_offset:x_offset+lw, c] +
                logo_alpha * logo_rgb[:, :, c]
            )
    else:
        image[y_offset:y_offset+lh, x_offset:x_offset+lw] = logo
    
    return image

def load_logo():
    return filedialog.askopenfilename(
        title="Selecteaza logo-ul",
        filetypes=[("PNG files", "*.png")]
    )

def load_template():
    return filedialog.askopenfilename(
        title="Selecteaza sablonul",
        filetypes=[("Imagini", "*.jpg;*.jpeg;*.png")]
    )

def load_image():
    return filedialog.askopenfilename(
        title="Selecteaza poza",
        filetypes=[("Imagini", "*.jpg;*.jpeg;*.png")]
    )

def main():
    root = tk.Tk()
    root.title("Editor Viniluri © Hodis Florin")

    template_path = None
    image_path = None
    logo_path = None
    logo = None
    result = None
    template_type = tk.StringVar(value="fata")
    extinde = tk.BooleanVar(value=False)
    aplicare_logo = tk.BooleanVar(value=False)

    canvas_template = tk.Canvas(root, width=600, height=400, bg="white")
    canvas_template.pack(side=tk.LEFT, padx=10, pady=10)

    def select_template():
        nonlocal template_path
        template_path = load_template()
        if template_path:
            img = Image.open(template_path)
            img_tk = ImageTk.PhotoImage(img)
            canvas_template.config(width=img_tk.width(), height=img_tk.height())
            canvas_template.create_image(0, 0, anchor=tk.NW, image=img_tk)
            canvas_template.image = img_tk
        update_preview()

    def select_image():
        nonlocal image_path
        image_path = load_image()
        update_preview()

    def select_logo():
        nonlocal logo_path, logo
        logo_path = load_logo()
        if logo_path:
            logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
            logo = resize_logo(logo)
        update_preview()
    
    def update_preview():
        nonlocal result
        if not template_path or not image_path:
            return
        # Coordonatele de aplicare a imaginii cu tot cu extindere
        coords = (157, 45, 498, 499) if template_type.get() == "fata" else (405, 45, 498, 499)
        if extinde.get():
            coords = (157, 45, 510, 505) if template_type.get() == "fata" else (395, 45, 510, 505)
    
        
        result = apply_template(template_path, image_path, coords)
        # Aplicare logo coordonate
        if aplicare_logo.get() and logo is not None:
            h, w, _ = result.shape
            if template_type.get() == "fata":
                x_offset = w - logo.shape[1] - (324 if not extinde.get() else 310)#daca scad valoarea lui else logo merge in dreapta
                y_offset = h - logo.shape[0] - 5
            else:
                x_offset = 323 if not extinde.get() else 312#daca scad valoarea lui else logo merge in dreapta
                y_offset = h - logo.shape[0] - 5
            result = apply_logo(result, logo, (x_offset, y_offset))
        
        result_bgr = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        result_img = Image.fromarray(result_bgr)
        result_tk = ImageTk.PhotoImage(result_img)
        canvas_template.create_image(0, 0, anchor=tk.NW, image=result_tk)
        canvas_template.image = result_tk
    
    def save_image():
        if result is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                filetypes=[("PNG files", "*.png")])
            if save_path:
                cv2.imwrite(save_path, result)
                messagebox.showinfo("Succes", f"Imaginea a fost salvata: {save_path}")
        else:
            messagebox.showerror("Eroare", "Nu exista nicio imagine de salvat.")
    
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    tk.Button(button_frame, text="Incarca Sablon", command=select_template).pack(pady=5)
    tk.Button(button_frame, text="Incarca Poza", command=select_image).pack(pady=5)
    tk.Button(button_frame, text="Incarca Logo", command=select_logo).pack(pady=5)
    tk.Button(button_frame, text="Salveaza", command=save_image).pack(pady=5)
    
    tk.Checkbutton(button_frame, text="Aplicare Logo", variable=aplicare_logo, command=update_preview).pack(pady=5)
    tk.Radiobutton(button_frame, text="Fata", variable=template_type, value="fata", command=update_preview).pack(pady=5)
    tk.Radiobutton(button_frame, text="Spate", variable=template_type, value="spate", command=update_preview).pack(pady=5)
    tk.Checkbutton(button_frame, text="Extinde", variable=extinde, command=update_preview).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
