import os, re
from pathlib import Path
from collections import defaultdict
import pytesseract
from PIL import Image
from lxml import etree
from unidecode import unidecode

# CONFIGURARE
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
INPUT_FOLDER = Path(r"C:\Users\User\Desktop\dictionarr")
IORDAN_FILE = Path(r"C:\Users\User\Desktop\iordan_curatat.txt")
OUTPUT_XML = Path(r"C:\Users\User\Desktop\dictionar_final.xml")

entries = defaultdict(lambda: {
    "lemma": "",
    "senses": [],
    "sources": set(),
    "dex_link": "",
    "clre_link": ""
})


# PARSER
def parse_onomastic(text, source):
    text = re.sub(r'[ \t]+', ' ', text)
    results = []
    # Caută Leamă + Definiție
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
    if not entry["lemma"]:
        entry["lemma"] = item["lemma"]
        entry["dex_link"] = f"https://dexonline.ro/definitie/{item['lemma'].lower()}"
        entry["clre_link"] = f"https://clre.ro/cautare?q={item['lemma'].lower()}"
    entry["sources"].add(item["source"])
    entry["senses"].append({"def": item["definition"], "source": item["source"]})


# PROCESARE
if __name__ == "__main__":
    # Procesare fișiere din folder (se bazează pe pytesseract direct)
    for file_path in INPUT_FOLDER.glob("*"):
        if file_path.suffix.lower() in ['.jpg', '.png', '.jpeg']:
            print(f"Procesez imagine: {file_path.name}")
            text = pytesseract.image_to_string(Image.open(file_path), lang="ron")
            for item in parse_onomastic(text, "Constantinescu"): merge_entry(item)

    # Procesare Iordan
    if IORDAN_FILE.exists():
        print("Procesez Iordan...")
        text = IORDAN_FILE.read_text(encoding="utf-8")
        for item in parse_onomastic(text, "Iordan"): merge_entry(item)

    # GENERARE XML
    root = etree.Element(f"{{{'http://www.tei-c.org/ns/1.0'}}}TEI")
    body = etree.SubElement(etree.SubElement(root, "text"), "body")

    for key, data in entries.items():
        entry = etree.SubElement(body, "entry")
        etree.SubElement(etree.SubElement(entry, "form"), "orth").text = data["lemma"]

        for s in data["senses"]:
            sense = etree.SubElement(entry, "sense")
            etree.SubElement(sense, "def").text = s["def"]
            etree.SubElement(sense, "bibl").text = s["source"]

        ext = etree.SubElement(entry, "external_data")
        etree.SubElement(ext, "dex_def").text = "DE_COMPLETAT"
        etree.SubElement(ext, "clre_def").text = "DE_COMPLETAT"
        etree.SubElement(ext, "dex_url").text = data["dex_link"]
        etree.SubElement(ext, "clre_url").text = data["clre_link"]

    etree.ElementTree(root).write(str(OUTPUT_XML), pretty_print=True, encoding="utf-8", xml_declaration=True)
    print(f"Gata! XML salvat la: {OUTPUT_XML}")