import xml.etree.ElementTree as ET
import re

input_file = r"C:\Users\User\Desktop\lexonomy_tei.xml"
output_file = r"C:\Users\User\Desktop\lexonomy_FINAL.xml"

TEI_NS = "http://www.tei-c.org/ns/1.0"
ns = {"tei": TEI_NS}
ET.register_namespace("", TEI_NS)

tree = ET.parse(input_file)
root = tree.getroot()

def is_noise(text):
    if not text:
        return True

    text = text.strip()

    if re.fullmatch(r"(A\s*){2,}", text):
        return True

    if re.fullmatch(r"[A-Za-zĂÂÎȘȚa-z]{1,3}", text):
        return True

    if not re.search(r"[aeiouăâîAEIOUĂÂÎ]", text):
        return True

    return False

removed = 0
kept = 0

# IMPORTANT: lucrăm pe părinte
body = root.find(".//tei:body", ns)

for entry in list(body.findall(".//tei:entry", ns)):

    orth = entry.find(".//tei:orth", ns)

    lemma = orth.text if (orth is not None and orth.text) else "".join(entry.itertext()).strip()

    if is_noise(lemma):
        body.remove(entry)   # ✅ FIX AICI (nu root)
        removed += 1
        continue

    # adaugă sursa dacă nu există
    if entry.find("tei:source", ns) is None:
        source = ET.Element(f"{{{TEI_NS}}}source")
        source.text = "Dicționar onomastic românesc – N. A. Constantinescu (1963)"
        entry.append(source)

    kept += 1

tree.write(output_file, encoding="utf-8", xml_declaration=True)

print("GATA")
print("Păstrate:", kept)
print("Eliminate:", removed)
print("Fișier:", output_file)