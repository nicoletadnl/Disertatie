from pathlib import Path
import pytesseract
from PIL import Image
import re

# ============================================
# CONFIG
# ============================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

INPUT_FOLDER = Path(
    r"C:\Users\User\Desktop\pages"
)

OUTPUT_TEXT = Path(
    r"C:\Users\User\Desktop\ocr_output.txt"
)

# ============================================
# OCR
# ============================================

all_text = []

images = sorted(INPUT_FOLDER.glob("*.jpg"))

print(f"Imagini găsite: {len(images)}\n")

for i, img_path in enumerate(images):

    print(f"OCR {i+1}/{len(images)} → {img_path.name}")

    try:

        img = Image.open(img_path)

        # grayscale
        img = img.convert("L")

        # binarizare
        img = img.point(
            lambda x: 0 if x < 140 else 255
        )

        text = pytesseract.image_to_string(
            img,
            lang="ron",
            config="--oem 1 --psm 4"
        )

        text = re.sub(r'[ \t]+', ' ', text)

        all_text.append(text)

    except Exception as e:

        print(f"EROARE: {e}")

OUTPUT_TEXT.write_text(
    "\n".join(all_text),
    encoding="utf-8"
)

print("\nGata.")
print(f"TXT salvat în:\n{OUTPUT_TEXT}")