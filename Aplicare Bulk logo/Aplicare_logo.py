import os
import cv2
import numpy as np
from tkinter import filedialog, Tk

def resize_logo(logo, target_size=80):
    h, w, _ = logo.shape
    scale = target_size / max(h, w)
    new_size = (int(w * scale), int(h * scale))
    return cv2.resize(logo, new_size, interpolation=cv2.INTER_AREA)

def apply_logo(image, logo, position):
    h, w, _ = image.shape
    lh, lw, _ = logo.shape
    x_offset, y_offset = position
    
    # Asigura-te că logo-ul incape în imagine
    x_offset = min(max(0, x_offset), w - lw)
    y_offset = min(max(0, y_offset), h - lh)
    
    # Aplica logo-ul cu transparenta
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

def preview_logo(image, logo, position):
    preview = apply_logo(image.copy(), logo, position)
    cv2.imshow("Previzualizare", preview)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return position

def process_images(input_folder, logo_path, output_folder):
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
    if logo is None:
        print("Eroare: Nu s-a putut încărca logo-ul.")
        return
    
    logo = resize_logo(logo)
    
    # Seteaza coordonatele pentru logo
    front_x_offset = 325  # Modifica pentru ajustarea poziției pe orizontală
    front_y_offset = 5   # Modifica pentru ajustarea poziției pe verticală
    back_x_offset = 325   # Modifica pentru ajustarea poziției pe orizontală
    back_y_offset = 5    # Modifica pentru ajustarea poziției pe verticală
    
    first_image = next((f for f in os.listdir(input_folder) if "_front" in f.lower()), None)
    if first_image:
        first_image_path = os.path.join(input_folder, first_image)
        image = cv2.imread(first_image_path)
        h, w, _ = image.shape
        front_position = (w - logo.shape[1] - front_x_offset, h - logo.shape[0] - front_y_offset)
        front_position = preview_logo(image, logo, front_position)
    
    first_back_image = next((f for f in os.listdir(input_folder) if "_back" in f.lower()), None)
    if first_back_image:
        first_back_path = os.path.join(input_folder, first_back_image)
        image = cv2.imread(first_back_path)
        h, w, _ = image.shape
        back_position = (back_x_offset, h - logo.shape[0] - back_y_offset)
        back_position = preview_logo(image, logo, back_position)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Eroare la citirea imaginii: {filename}")
                continue
            
            if "_front" in filename.lower():
                position = front_position
            elif "_back" in filename.lower():
                position = back_position
            else:
                print(f"Skipping {filename}: nu este clar dacă este față sau spate.")
                continue
            
            result = apply_logo(image, logo, position)
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, result)
            print(f"Salvat: {output_path}")

def main():
    Tk().withdraw()
    input_folder = filedialog.askdirectory(title="Selectează folderul cu imagini")
    logo_path = filedialog.askopenfilename(title="Selectează logo-ul", filetypes=[("Image files", "*.png;*.jpg")])
    output_folder = filedialog.askdirectory(title="Selectează folderul pentru salvare")
    
    if not all([input_folder, logo_path, output_folder]):
        print("Selecție invalidă, verifică folderele și fișierele.")
        return
    
    process_images(input_folder, logo_path, output_folder)
    
if __name__ == "__main__":
    main()
