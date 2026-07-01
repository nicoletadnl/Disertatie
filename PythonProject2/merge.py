import xml.etree.ElementTree as ET
import re
from collections import defaultdict

# ==========================
# FIȘIERE
# ==========================
file_iordan = r"C:\Users\User\Desktop\iordan_STRUCTURAT.xml"
file_const = r"C:\Users\User\Desktop\lexonomy_FINAL.xml"
output_file = r"C:\Users\User\Desktop\DICTIONAR_FINAL_CORECT.xml"

# ==========================
# TEI
# ==========================
TEI_NS = "http://www.tei-c.org/ns/1.0"
ns = {"tei": TEI_NS}
ET.register_namespace("", TEI_NS)

# ==========================
# CURĂȚARE LEMĂ
# ==========================
def clean_lemma(text):
    if not text:
        return None

    text = text.strip()

    # elimină zgomot OCR
    if re.search(r"[^A-Za-zĂÂÎȘȚăâîșț\- ]", text):
        return None

    if re.search(r"\d", text):
        return None

    if len(text) < 3:
        return None

    return text

# ==========================
# CURĂȚARE DEFINIȚIE
# ==========================
def clean_def(text):
    if not text:
        return None

    text = text.strip()

    if len(text) < 8:
        return None

    text = re.sub(r"[<>]", "", text)
    text = re.sub(r"&[a-zA-Z0-9#]+;", "", text)
    text = re.sub(r"\s+", " ", text)

    return text

# ==========================
# STRUCTURĂ FINALĂ
# ==========================
dictionary = defaultdict(lambda: {"Iordan": [], "Constantinescu": []})

# ==========================
# PARSARE FIȘIER
# ==========================
def process_file(path, source_name):
    tree = ET.parse(path)
    root = tree.getroot()

    for entry in root.findall(".//tei:entry", ns):

        orth = entry.find(".//tei:orth", ns)
        lemma = clean_lemma(orth.text if orth is not None else None)

        if not lemma:
            continue

        defs = entry.findall(".//tei:def", ns)

        clean_defs = []
        for d in defs:
            if d.text:
                c = clean_def(d.text)
                if c:
                    clean_defs.append(c)

        if not clean_defs:
            continue

        dictionary[lemma][source_name].append(" | ".join(clean_defs))

# ==========================
# RUN
# ==========================
process_file(file_iordan, "Iordan")
process_file(file_const, "Constantinescu")

# ==========================
# CONSTRUCȚIE TEI FINAL
# ==========================
root = ET.Element(f"{{{TEI_NS}}}TEI")
text = ET.SubElement(root, f"{{{TEI_NS}}}text")
body = ET.SubElement(text, f"{{{TEI_NS}}}body")

for lemma, data in sorted(dictionary.items()):

    entry = ET.SubElement(body, f"{{{TEI_NS}}}entry")

    form = ET.SubElement(entry, f"{{{TEI_NS}}}form")
    orth = ET.SubElement(form, f"{{{TEI_NS}}}orth")
    orth.text = lemma.upper()

    sense = ET.SubElement(entry, f"{{{TEI_NS}}}sense")

    # ==========================
    # IORDAN
    # ==========================
    for d in data["Iordan"]:
        def_el = ET.SubElement(sense, f"{{{TEI_NS}}}def")
        def_el.text = d

        cit = ET.SubElement(sense, f"{{{TEI_NS}}}cit", {"type": "source"})
        bibl = ET.SubElement(cit, f"{{{TEI_NS}}}bibl")
        bibl.text = "Iordan"

    # ==========================
    # CONSTANTINESCU
    # ==========================
    for d in data["Constantinescu"]:
        def_el = ET.SubElement(sense, f"{{{TEI_NS}}}def")
        def_el.text = d

        cit = ET.SubElement(sense, f"{{{TEI_NS}}}cit", {"type": "source"})
        bibl = ET.SubElement(cit, f"{{{TEI_NS}}}bibl")
        bibl.text = "Constantinescu"

# ==========================
# SALVARE
# ==========================
ET.ElementTree(root).write(output_file, encoding="utf-8", xml_declaration=True)

print("GATA FINAL COMPLET")
print("Fișier:", output_file)
print("Leme unice:", len(dictionary))