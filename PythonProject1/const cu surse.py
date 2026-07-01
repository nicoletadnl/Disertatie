from lxml import etree
from pathlib import Path

DIR_LUCRU = Path.home() / "Desktop"
F_CONSTANTINESCU = DIR_LUCRU / "lexonomy_tei.xml"
F_OUTPUT = DIR_LUCRU / "LEXONOMY_AVANSAT_FINAL.xml"


def creeaza_xml_lexonomy_perfect():
    # Citim fișierul sursă
    tree = etree.parse(str(F_CONSTANTINESCU))
    root = etree.Element("root")

    for entry in tree.xpath('//entry'):
        orth_node = entry.find('orth')
        if orth_node is None: continue

        # Creăm intrarea
        new_entry = etree.SubElement(root, "entry")
        etree.SubElement(new_entry, "orth").text = orth_node.text

        # 1. Container: Sursa Bază (Constantinescu)
        base = etree.SubElement(new_entry, "base_source")
        etree.SubElement(base, "name").text = "Constantinescu"
        def_node = entry.find('.//def')
        etree.SubElement(base, "def").text = def_node.text if def_node is not None else ""

        # 2. Listă: Resurse Externe (Gata de populat)
        # Lexonomy va vedea acest tag ca o listă dacă îl configurezi corect
        ext_resources = etree.SubElement(new_entry, "external_resources")

        # Adăugăm un element gol (placeholder) pentru a fi sigur că Lexonomy vede structura
        res = etree.SubElement(ext_resources, "resource")
        etree.SubElement(res, "name").text = ""
        etree.SubElement(res, "link").text = ""
        etree.SubElement(res, "nlp_metadata").text = ""

    # Salvăm fișierul
    etree.ElementTree(root).write(str(F_OUTPUT), pretty_print=True, encoding="utf-8", xml_declaration=True)
    print(f"Fișierul perfect pentru import a fost generat: {F_OUTPUT}")


if __name__ == "__main__":
    creeaza_xml_lexonomy_perfect()