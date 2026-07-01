import os
import pytesseract
from PIL import Image

# =========================
# TESSERACT PATH (OBLIGATORIU)
# =========================
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# =========================
# FOLDERE INPUT
# =========================
iordan_folder = r"C:\Users\User\Desktop\disertatie\mostra Iordan"
const_folder = r"C:\Users\User\Desktop\disertatie\mostra Const"

# =========================
# OUTPUT
# =========================
output_folder = r"C:\Users\User\Desktop\disertatie\output"
os.makedirs(output_folder, exist_ok=True)

output_iordan = os.path.join(output_folder, "iordan_raw.txt")
output_const = os.path.join(output_folder, "constantinescu_raw.txt")

# =========================
# OCR FUNCTION
# =========================
def ocr_folder(folder_path, output_file):
    text_total = ""

    files = sorted(os.listdir(folder_path))

    for file in files:
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(folder_path, file)
        print("OCR:", file)

        img = Image.open(path)

        text = pytesseract.image_to_string(img, lang="ron")

        text_total += "\n" + text + "\n"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text_total)


# =========================
# RUN OCR
# =========================
ocr_folder(iordan_folder, output_iordan)
ocr_folder(const_folder, output_const)

print("GATA OCR COMPLET")
print("Iordan:", output_iordan)
print("Constantinescu:", output_const)