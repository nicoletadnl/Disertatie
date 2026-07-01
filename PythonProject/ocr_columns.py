from pathlib import Path
from PIL import Image
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

INPUT_FOLDER = Path(r"C:\Users\User\Desktop\jpg_dictionar")
OUTPUT_FILE = Path(r"C:\Users\User\Desktop\ocr_output.txt")

images = sorted(INPUT_FOLDER.glob("*.jpg"))

all_text = []

print(f"Imagini găsite: {len(images)}")

for i, img_path in enumerate(images):

    print(f"OCR {i+1}/{len(images)} -> {img_path.name}")

    img = Image.open(img_path)

    # IMPORTANT: preprocesare simplă
    img = img.convert("L")

    # OCR pentru layout pe 2 coloane
    text = pytesseract.image_to_string(
        img,
        lang="ron",
        config="--oem 1 --psm 1"
    )

    # curățare de bază
    text = re.sub(r'[ \t]+', ' ', text)

    all_text.append(text)

OUTPUT_FILE.write_text("\n".join(all_text), encoding="utf-8")

print("GATA OCR")
print(OUTPUT_FILE)