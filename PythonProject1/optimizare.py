from lxml import etree
from pathlib import Path
from collections import defaultdict

# --- CONFIGURARE ---
DIR_LUCRU = Path.home() / "Desktop"
F_OUTPUT = DIR_LUCRU / "DICTIONAR_TOTAL_AVANSAT.xml"

# Structura surselor externe
EXT_RESOURCES = [
    {"nume": "Iordan", "link": ""},
    {"nume": "Oxford Dictionary of First Names",
     "link": "https://global.oup.com/academic/product/a-dictionary-of-first-names-9780198800514"},
    {"nume": "Lexilogos", "link": "https://www.lexilogos.com/noms_famille.htm"},
    {"nume": "Cognomix", "link": "https://www.cognomix.it"},
    {"nume": "FamilySearch", "link": "https://www.familysearch.org/en/global"},
    {"nume": "Ancestry", "link": "https://www.ancestry.com"},
    {"nume": "MyHeritage", "link": "https://www.myheritage.com"},
    {"nume": "Forebears", "link": "https://forebears.io"},
    {"nume": "Geneanet", "link": "https://en.geneanet.org"},
    {"nume": "Arhivele Nationale", "link": "https://arhivelenationale.ro"},
    {"nume": "HuggingFace/NLP", "link": "https://huggingface.co"},
    {"nume": "WSD/NER Service", "link": "local_nlp_pipeline"}
]


def genereaza_xml_avansat():
    root = etree.Element("root")
    # Aici presupunem că baza ta de date unificată este pregătită
    # Vom crea o structură care să poată fi completată

    entry = etree.SubElement(root, "entry")
    etree.SubElement(entry, "orth").text = "EXEMPLU"  # Lema

    # 1. Sursa Principală
    base = etree.SubElement(entry, "base_source")
    etree.SubElement(base, "name").text = "Constantinescu"
    etree.SubElement(base, "def").text = "Definiția din Constantinescu..."

    # 2. Resurse Externe
    ext_section = etree.SubElement(entry, "external_resources")
    for res in EXT_RESOURCES:
        item = etree.SubElement(ext_section, "resource")
        etree.SubElement(item, "name").text = res["nume"]
        etree.SubElement(item, "link").text = res["link"]
        etree.SubElement(item, "status").text = "link_valid"

    etree.ElementTree(root).write(str(F_OUTPUT), pretty_print=True, encoding="utf-8", xml_declaration=True)
    print(f"Structură avansată creată: {F_OUTPUT}")


if __name__ == "__main__":
    genereaza_xml_avansat()