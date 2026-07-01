import re
import xml.etree.ElementTree as ET

input_file = r"C:\Users\User\Desktop\disertatie\output\iordan_raw.txt"
output_file = r"C:\Users\User\Desktop\disertatie\output\iordan.xml"

TEI_NS = "http://www.tei-c.org/ns/1.0"
ET.register_namespace("", TEI_NS)

# =========================
# DETECTARE LEMĂ (mai robust)
# =========================
def is_lemma(line):
    line = line.strip()

    if len(line) < 2:
        return False

    if re.search(r"\d", line):
        return False

    # Iordan: cuvânt la început de bloc
    return bool(re.match(r"^[A-ZĂÂÎȘȚ][a-zăâîșț\-]+", line))

# =========================
# ÎNCĂRCARE TEXT COMPLET
# =========================
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# =========================
# NORMALIZARE
# =========================
text = re.sub(r"\n+", "\n", text)

lines = text.split("\n")

entries = []
current = None

# =========================
# PARSARE PE BLOCS
# =========================
for line in lines:

    line = line.strip()
    if not line:
        continue

    if is_lemma(line):

        if current:
            entries.append(current)

        current = {
            "lemma": line.split()[0].upper(),
            "text": []
        }

    else:
        if current:
            current["text"].append(line)

if current:
    entries.append(current)

# =========================
# XML
# =========================
root = ET.Element(f"{{{TEI_NS}}}TEI")
text_el = ET.SubElement(root, f"{{{TEI_NS}}}text")
body = ET.SubElement(text_el, f"{{{TEI_NS}}}body")

for e in entries:

    entry = ET.SubElement(body, f"{{{TEI_NS}}}entry")

    form = ET.SubElement(entry, f"{{{TEI_NS}}}form")
    orth = ET.SubElement(form, f"{{{TEI_NS}}}orth")
    orth.text = e["lemma"]

    sense = ET.SubElement(entry, f"{{{TEI_NS}}}sense")

    def_text = " ".join(e["text"])

    d = ET.SubElement(sense, f"{{{TEI_NS}}}def")
    d.text = def_text

    cit = ET.SubElement(sense, f"{{{TEI_NS}}}cit", {"type": "source"})
    bibl = ET.SubElement(cit, f"{{{TEI_NS}}}bibl")
    bibl.text = "Iordan"

ET.ElementTree(root).write(output_file, encoding="utf-8", xml_declaration=True)

print("GATA IORDAN v3")
print("Intrări:", len(entries))
