import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.ndimage import binary_closing


cale_folder = r'C:\Users\alexa\Desktop\TSIM'
lista_imagini = [f for f in os.listdir(cale_folder) if f.endswith('.bmp')]

def show_result(title, image):
    plt.figure()
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()


for nume_imagine in lista_imagini:
    print(f'Procesez {nume_imagine}...')
    cale_img = os.path.join(cale_folder, nume_imagine)
    img_color = plt.imread(cale_img)


    if img_color.ndim == 3:
        img = np.dot(img_color[..., :3], [0.2989, 0.5870, 0.1140])
    else:
        img = img_color

    img = (img * 255) if img.max() <= 1.0 else img
    img = img.astype(np.uint8)

    # === 1. Funcția LOGARITMICĂ ===
    c_log = 255 / np.log(1 + np.max(img))
    log_img = c_log * np.log(1 + img.astype(np.float32))
    log_img = np.uint8(np.clip(log_img, 0, 255))
    show_result(f"{nume_imagine} - Transformare Logaritmică", log_img)

    # === 2. Funcția PUTERE CU PUNCT FIX ===
    gamma_fp = 2.0
    fp_img = np.power(img.astype(np.float32) / 255.0, gamma_fp)
    fp_img = np.uint8(np.clip(fp_img * 255, 0, 255))
    show_result(f"{nume_imagine} - Putere cu punct fix (Gamma = {gamma_fp})", fp_img)

    # === 3. Funcția CLIPPING ===
    low, high = 50, 200
    clipped = np.clip(img, low, high)
    clipped = ((clipped - low) / (high - low)) * 255
    clipped = np.uint8(np.clip(clipped, 0, 255))
    show_result(f"{nume_imagine} - Clipping ({low}–{high})", clipped)

    # === 4. Slicing ===
    low_s, high_s = 100, 180
    constanta = 1
    sliced = np.where((img >= low_s) & (img <= high_s), constanta, 0).astype(np.uint8)
    show_result(f"{nume_imagine} - Slicing ({low_s}-{high_s})", sliced)

    # === 5. Închidere morfologică ===
    sliced_bool = sliced.astype(bool)
    structura = np.ones((3, 3), dtype=bool)
    inchidere = binary_closing(sliced_bool, structure=structura)
    inchidere_uint8 = (inchidere.astype(np.uint8)) * 255
    show_result(f"{nume_imagine} - Închidere morfologică", inchidere_uint8)

