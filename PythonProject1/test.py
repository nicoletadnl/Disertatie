import re
from lxml import etree
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# --- CONFIGURARE ---
DIR_LUCRU = Path.home() / "Desktop"
F_CONSTANTINESCU = DIR_LUCRU / "lexonomy_tei.xml"
F_IORDAN_TEI = DIR_LUCRU / "iordan_STRUCTURAT.xml"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
F_OUTPUT = DIR_LUCRU / f"dictionar_UNIFICAT_{timestamp}.xml"


def curata_lema(text):
    if not text: return None
    text_fara_taguri = re.sub(r'<[^>]+>', '', text)
    t = re.sub(r'[^A-Za-zĂÂÎȘȚăâîșț]', '', text_fara_taguri)
    return t.upper() if t else None


def unifica_tot():
    baza_date = defaultdict(dict)

    for file_path, bibl_val in [(F_CONSTANTINESCU, "Constantinescu"), (F_IORDAN_TEI, "Iordan")]:
        if not file_path.exists(): continue

        tree = etree.parse(str(file_path))

        # DEBUG: Afișăm ce găsim în fișierul Iordan
        if bibl_val == "Iordan":
            intrari = tree.xpath('//*[local-name()="entry"]')
            print(f"DEBUG: Am găsit {len(intrari)} intrări în Iordan.")
            if intrari:
                print(f"DEBUG: Exemplu: {etree.tostring(intrari[0], encoding='unicode')}")

        for entry in tree.xpath('//*[local-name()="entry"]'):
            orth_nodes = entry.xpath('.//*[local-name()="orth"]')
            defn_nodes = entry.xpath('.//*[local-name()="def"]')

            if orth_nodes and orth_nodes[0].text:
                lema = curata_lema(orth_nodes[0].text)
                if not lema: continue

                text_def = "".join(defn_nodes[0].itertext()).strip() if defn_nodes else ""

                if bibl_val in baza_date[lema]:
                    baza_date[lema][bibl_val] += " | " + text_def
                else:
                    baza_date[lema][bibl_val] = text_def

    # Generare (restul codului rămâne la fel)
    root = etree.Element("root")
    for lema in sorted(baza_date.keys()):
        new_entry = etree.SubElement(root, "entry")
        etree.SubElement(new_entry, "orth").text = lema
        for sursa, text_def in baza_date[lema].items():
            sense = etree.SubElement(new_entry, "sense")
            etree.SubElement(sense, "bibl").text = sursa
            etree.SubElement(sense, "def").text = text_def

    etree.ElementTree(root).write(str(F_OUTPUT), pretty_print=True, encoding="utf-8", xml_declaration=True)
    print(f"Finalizat! Intrări unificate: {len(baza_date)}")


if __name__ == "__main__":
    unifica_tot()