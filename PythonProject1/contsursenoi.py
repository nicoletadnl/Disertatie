from lxml import etree
from pathlib import Path

DIR_LUCRU = Path.home() / "Desktop"
F_INTRARE = DIR_LUCRU / "lexonomy_tei.xml"
F_IESIRE = DIR_LUCRU / "noudictionar.xml"

# Doar 7 resurse (jumătate din cele 15 inițiale)
RESURSE_SELECTATE = [
    "Iordan", "Oxford Dictionary of First Names", "Lexilogos",
    "Cognomix", "FamilySearch", "Ancestry", "MyHeritage"
]


def genereaza_dictionar_simplificat():
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    tree = etree.parse(str(F_INTRARE))
    root_nou = etree.Element("root")

    for entry in tree.xpath('//tei:entry', namespaces=ns):
        # Extragem datele din structura TEI
        orth_node = entry.xpath('.//tei:form/tei:orth', namespaces=ns)
        def_node = entry.xpath('.//tei:sense/tei:def', namespaces=ns)

        orth_text = orth_node[0].text if orth_node else "N/A"
        def_text = def_node[0].text if def_node else "N/A"

        # Construim noua structură
        new_entry = etree.SubElement(root_nou, "entry")
        etree.SubElement(new_entry, "orth").text = orth_text

        # Sursa Constantinescu (cum ai văzut în image_81da9d.png)
        base = etree.SubElement(new_entry, "base_source")
        etree.SubElement(base, "name").text = "Constantinescu"
        etree.SubElement(base, "def").text = def_text

        # Resurse externe (jumătate din listă)
        ext = etree.SubElement(new_entry, "external_resources")
        for res_name in RESURSE_SELECTATE:
            res = etree.SubElement(ext, "resource")
            etree.SubElement(res, "name").text = res_name
            etree.SubElement(res, "link").text = ""

    etree.ElementTree(root_nou).write(str(F_IESIRE), pretty_print=True, encoding="utf-8", xml_declaration=True)
    print(f"Dicționarul 'noudictionar' a fost generat pe Desktop.")


if __name__ == "__main__":
    genereaza_dictionar_simplificat()