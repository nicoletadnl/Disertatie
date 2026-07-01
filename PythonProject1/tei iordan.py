import re
from lxml import etree
from pathlib import Path

# Setează calea către fișierul tău
FILE_IN = Path.home() / "Desktop" / "iordan mostra.txt"
FILE_OUT = Path.home() / "Desktop" / "iordan_STRUCTURAT.xml"


def creeaza_xml_iordan():
    root = etree.Element("root")

    # Citim fișierul cu encoding utf-8
    with open(FILE_IN, "r", encoding="utf-8") as f:
        linii = f.readlines()

    for linie in linii:
        linie = linie.strip()
        if not linie: continue

        # Regex: caută textul de la începutul liniei până la primul semn de punctuație
        match = re.match(r'^([A-ZĂÂÎȘȚa-zâîșț]+)[:\.]?\s*(.*)', linie)
        if match:
            lema = match.group(1).upper()
            definitie = match.group(2)

            entry = etree.SubElement(root, "entry")
            etree.SubElement(entry, "orth").text = lema
            def_node = etree.SubElement(entry, "def")
            def_node.text = definitie

    etree.ElementTree(root).write(str(FILE_OUT), pretty_print=True, encoding="utf-8", xml_declaration=True)
    print(f"Succes! Fișierul structurat a fost creat: {FILE_OUT}")


if __name__ == "__main__":
    creeaza_xml_iordan()