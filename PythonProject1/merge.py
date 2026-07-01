import os, re, io
from pathlib import Path
from collections import defaultdict
import fitz, pytesseract
from PIL import Image
from lxml import etree
from unidecode import unidecode

# CONFIG
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
INPUT_PDF = Path(r"C:\Users\User\Desktop\dictionarr")
INPUT_JPG = Path(r"C:\Users\User\Desktop\jpg_dictionar")
IORDAN_FILE = Path(r"C:\Users\User\Desktop\iordan_curatat.txt")
OUTPUT_XML = Path(r"C:\Users\User\Desktop\dictionar_final_complet.xml")

entries = defaultdict(lambda: {"lemma": "", "forms": set(), "senses": [], "sources": set(), "links": set()})


# PARSER
def parse_onomastic(text, source):
    # Curățare
    text = re.sub(r'[ \t]+', ' ', text)
    results = []
    # Pattern pentru lemă (cuvânt) și definiție
    pattern = re.compile(r'^\s*([A-ZĂÂÎȘȚ\-]+)\s+(.+?)(?=\n[A-ZĂÂÎȘȚ\-]+\s|\Z)', re.MULTILINE | re.DOTALL)

    for match in pattern.finditer(text):
        lemma = match.group(1).strip()
        definition = match.group(2).strip()

        if len(lemma) < 2 or len(definition) < 5: continue

        results.append({"lemma": lemma, "definition": definition, "source": source})
    return results


def merge_entry(item):
    key = unidecode(item["lemma"].lower())
    entry = entries[key]
    if not entry["lemma"]: entry["lemma"] = item["lemma"]
    entry["sources"].add(item["source"])
    entry["senses"].append({"def": item["definition"], "source": item["source"]})
    # Link automat DEXonline
    entry["links"].add(f"https://dexonline.ro/definitie/{item['lemma'].lower()}")


# PROCESARE
if __name__ == "__main__":
    # 1. PDF-uri
    for pdf in INPUT_PDF.glob("*.pdf"):
        print(f"Procesez PDF: {pdf.name}")
        doc = fitz.open(pdf)
        for page in doc:
            img = Image.open(io.BytesIO(page.get_pixmap(dpi=300).tobytes("png")))
            text = pytesseract.image_to_string(img, lang="ron", config="--psm 4")
            for item in parse_onomastic(text, "Constantinescu"): merge_entry(item)

    # 2. JPG-uri
    for jpg in INPUT_JPG.glob("*.jpg"):
        print(f"Procesez JPG: {jpg.name}")
        text = pytesseract.image_to_string(Image.open(jpg), lang="ron", config="--psm 4")
        for item in parse_onomastic(text, "Constantinescu"): merge_entry(item)

    # 3. Iordan (deja curatat)
    if IORDAN_FILE.exists():
        print("Procesez Iordan...")
        for item in parse_onomastic(IORDAN_FILE.read_text(encoding="utf-8"), "Iordan"):
            merge_entry(item)

    # GENERARE XML (Structura TEI)
    root = etree.Element(f"{{{'http://www.tei-c.org/ns/1.0'}}}TEI")
    body = etree.SubElement(etree.SubElement(root, "text"), "body")

    for key, data in entries.items():
        entry = etree.SubElement(body, "entry")
        orth = etree.SubElement(etree.SubElement(entry, "form"), "orth")
        orth.text = data["lemma"]
        for s in data["senses"]:
            def_el = etree.SubElement(etree.SubElement(entry, "sense"), "def")
            def_el.text = s["def"]
            etree.SubElement(entry, "bibl").text = s["source"]
        for l in data["links"]:
            etree.SubElement(entry, "ref", target=l).text = "DEXonline"

    etree.ElementTree(root).write(str(OUTPUT_XML), pretty_print=True, encoding="utf-8", xml_declaration=True)
    print(f"Gata! XML salvat la: {OUTPUT_XML}")