import pytesseract
from PIL import Image
from pathlib import Path
import re

# Setări
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Folderul tău cu imagini din imagine_62f8a5.png
INPUT_FOLDER = Path(r"C:\Users\User\Desktop\disertatie\iordan.1")
OUTPUT_TEXT = Path(r"C:\Users\User\Desktop\iordan_ocr_imagini.txt")

# Căutăm toate fișierele de tip imagine
imagine_files = sorted(list(INPUT_FOLDER.glob("*.*")))
all_text = []

for img_path in imagine_files:
    # Verificăm dacă e un format de imagine suportat
    if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
        print(f"Procesez imaginea: {img_path.name}...")
        try:
            # Deschidem imaginea
            img = Image.open(img_path)

            # OCR pe imagine
            text = pytesseract.image_to_string(img, lang="ron", config="--psm 6")
            text = re.sub(r'[ \t]+', ' ', text)
            all_text.append(f"\n--- {img_path.name} ---\n{text}")
            print(f"  - Finalizat.")
        except Exception as e:
            print(f"EROARE la {img_path.name}: {e}")

# Salvarea rezultatului
OUTPUT_TEXT.write_text("\n".join(all_text), encoding="utf-8")
print(f"Gata! Text salvat în: {OUTPUT_TEXT}")