from lxml import etree
from pathlib import Path
from collections import defaultdict
import datetime

# Configurare căi
FILE_CONSTANTINESCU = Path(r"C:\Users\User\Desktop\lexonomy_tei.xml")
FILE_IORDAN = Path(r"C:\Users\User\Desktop\iordan_curatat.txt")  # Am actualizat extensia
OUTPUT_XML = Path(r"C:\Users\User\Desktop\dictionar_unificat_final.xml")


def get_normalized_lemma(text):
    return text.strip().upper() if text else ""


def merge_and_fix():
    master_data = defaultdict(list)

    # 1. Procesare Constantinescu (XML)
    if FILE_CONSTANTINESCU.exists():
        tree = etree.parse(str(FILE_CONSTANTINESCU))
        for entry in tree.xpath('//*[local-name()="entry"]'):
            orth = entry.xpath('.//*[local-name()="orth"]')
            if not orth: continue
            lemma = get_normalized_lemma(orth[0].text)
            for def_node in entry.xpath('.//*[local-name()="def"]'):
                if def_node.text:
                    master_data[lemma].append({"def": def_node.text.strip(), "source": "Constantinescu"})

    # 2. Procesare Iordan (Text simplu)
    if FILE_IORDAN.exists():
        with open(FILE_IORDAN, "r", encoding="utf-8") as f:
            for line in f:
                if "\t" in line:
                    parts = line.split("\t", 1)
                    lemma = get_normalized_lemma(parts[0])
                    defn = parts[1].strip()
                    master_data[lemma].append({"def": defn, "source": "Iordan"})

    # 3. Construire XML final
    root = etree.Element("TEI")
    body = etree.SubElement(etree.SubElement(root, "text"), "body")

    for lemma, senses in master_data.items():
        entry = etree.SubElement(body, "entry")
        etree.SubElement(etree.SubElement(entry, "form"), "orth").text = lemma

        for s in senses:
            sense = etree.SubElement(entry, "sense")
            etree.SubElement(sense, "def").text = s["def"]
            etree.SubElement(sense, "bibl").text = s["source"]

        # Date externe
        ext = etree.SubElement(entry, "external_data")
        etree.SubElement(ext, "dex_url").text = f"https://dexonline.ro/definitie/{lemma.lower()}"
        etree.SubElement(ext, "dex_def").text = "DE_COMPLETAT"

        # Metadate
        meta = etree.SubElement(entry, "metadata")
        etree.SubElement(meta, "date").text = datetime.date.today().isoformat()

    etree.ElementTree(root).write(str(OUTPUT_XML), pretty_print=True, encoding="utf-8", xml_declaration=True)
    print(f"Gata! Iordan a fost inclus. Fișier: {OUTPUT_XML}")


if __name__ == "__main__":
    merge_and_fix()