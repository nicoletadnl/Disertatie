import os
import re
import pytesseract
from PIL import Image
import xml.etree.ElementTree as ET

# =========================
# TESSERACT PATH
# =========================
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# =========================
# INPUT IMAGES
# =========================
folder = r"C:\Users\User\Desktop\disertatie\mostra Const"

# =========================
# OUTPUT
# =========================
output_txt = r"C:\Users\User\Desktop\disertatie\output\constantinescu_raw.txt"
output_xml = r"C:\Users\User\Desktop\disertatie\output\constantinescu.xml"

os.makedirs(os.path.dirname(output_txt), exist_ok=True)

# =========================
# OCR
# =========================
def run_ocr(folder):
    text = ""

    files = sorted(os.listdir(folder))

    for f in files:
        if not f.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(folder, f)
        print("OCR:", f)

        img = Image.open(path)

        txt = pytesseract.image_to_string(img, lang="ron")

        text += "\n" + txt + "\n"

    with open(output_txt, "w", encoding="utf-8") as g:
        g.write(text)

# =========================
# PARSARE CONSTANTINESCU
# =========================
def parse_text(text):
    entries = []

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    for line in lines:

        # eliminăm zgomot
        if len(line) < 2:
            continue
        if re.search(r"www|http|\d{3,}", line.lower()):
            continue

        # format principal: LEMĂ < DEFINIȚIE
        if "<" in line:
            parts = line.split("<", 1)
            lemma = parts[0].strip()
            definition = parts[1].strip()

            entries.append({
                "lemma": lemma,
                "def": definition
            })

        # fallback (dacă OCR rupe linia)
        elif re.match(r"^[A-Za-zĂÂÎȘȚăâîșț]+", line):
            parts = line.split(" ", 1)
            lemma = parts[0]
            definition = parts[1] if len(parts) > 1 else ""

            entries.append({
                "lemma": lemma,
                "def": definition
            })

    return entries

# =========================
# XML GENERATOR
# =========================
def to_xml(entries):
    TEI_NS = "http://www.tei-c.org/ns/1.0"
    ET.register_namespace("", TEI_NS)

    root = ET.Element(f"{{{TEI_NS}}}TEI")
    text_el = ET.SubElement(root, f"{{{TEI_NS}}}text")
    body = ET.SubElement(text_el, f"{{{TEI_NS}}}body")

    for e in entries:

        entry = ET.SubElement(body, f"{{{TEI_NS}}}entry")

        form = ET.SubElement(entry, f"{{{TEI_NS}}}form")
        orth = ET.SubElement(form, f"{{{TEI_NS}}}orth")
        orth.text = e["lemma"]

        sense = ET.SubElement(entry, f"{{{TEI_NS}}}sense")

        d = ET.SubElement(sense, f"{{{TEI_NS}}}def")
        d.text = e["def"]

        cit = ET.SubElement(sense, f"{{{TEI_NS}}}cit", {"type": "source"})
        bibl = ET.SubElement(cit, f"{{{TEI_NS}}}bibl")
        bibl.text = "Constantinescu"

    ET.ElementTree(root).write(output_xml, encoding="utf-8", xml_declaration=True)

# =========================
# RUN FULL PIPELINE
# =========================
run_ocr(folder)

with open(output_txt, "r", encoding="utf-8") as f:
    text = f.read()

entries = parse_text(text)

to_xml(entries)

print("GATA CONSTANTINESCU PIPELINE")
print("Intrări:", len(entries))
print("TXT:", output_txt)
print("XML:", output_xml)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"