from lxml import etree
from pathlib import Path

# Configurare căi
FILE_CONSTANTINESCU = Path(r"C:\Users\User\Desktop\lexonomy_tei.xml")
FILE_IORDAN = Path(r"C:\Users\User\Desktop\dictionar_final.xml")
OUTPUT_XML = Path(r"C:\Users\User\Desktop\dictionar_complet_unificat.xml")


def merge_dictionaries():
    NS = {"tei": "http://www.tei-c.org/ns/1.0"}
    root = etree.Element(f"{{{NS['tei']}}}TEI")
    body = etree.SubElement(etree.SubElement(root, "text"), "body")

    dict_data = {}  # Folosim un dicționar pentru a grupa sensurile pe leme

    # Funcție de procesare
    def process_file(file_path, source_name):
        if not file_path.exists(): return
        tree = etree.parse(str(file_path))
        for entry in tree.xpath('//tei:entry', namespaces=NS):
            orth = entry.find('.//tei:orth', namespaces=NS)
            if orth is None: continue
            lemma = orth.text.lower()

            if lemma not in dict_data:
                dict_data[lemma] = {"lemma": orth.text, "senses": []}

            # Extragem definițiile din fișierul respectiv
            for sense in entry.xpath('.//tei:sense', namespaces=NS):
                def_text = sense.find('.//tei:def', namespaces=NS).text
                dict_data[lemma]["senses"].append({"def": def_text, "source": source_name})

    # Procesăm ambele surse
    process_file(FILE_CONSTANTINESCU, "Constantinescu")
    process_file(FILE_IORDAN, "Iordan")

    # Generăm XML-ul final
    for lemma, data in dict_data.items():
        entry = etree.SubElement(body, "entry")
        etree.SubElement(etree.SubElement(entry, "form"), "orth").text = data["lemma"]

        for s in data["senses"]:
            sense = etree.SubElement(entry, "sense")
            etree.SubElement(sense, "def").text = s["def"]
            etree.SubElement(sense, "bibl").text = s["source"]  # Aici apare sursa în Lexonomy

        # Secțiune dedicată pentru completare manuală
        ext = etree.SubElement(entry, "external_data")
        etree.SubElement(ext, "dex_def").text = "DE_COMPLETAT"
        etree.SubElement(ext, "clre_def").text = "DE_COMPLETAT"
        etree.SubElement(ext, "dex_url").text = f"https://dexonline.ro/definitie/{lemma}"
        etree.SubElement(ext, "clre_url").text = f"https://clre.ro/cautare?q={lemma}"

    etree.ElementTree(root).write(str(OUTPUT_XML), pretty_print=True, encoding="utf-8", xml_declaration=True)
    print(f"Succes! Dicționar unificat salvat la: {OUTPUT_XML}")


if __name__ == "__main__":
    merge_dictionaries()