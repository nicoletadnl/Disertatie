import re
import xml.etree.ElementTree as ET

input_file = r"C:\Users\User\Desktop\disertatie\output\iordan_raw.txt"
output_file = r"C:\Users\User\Desktop\disertatie\output\iordan.xml"

TEI_NS = "http://www.tei-c.org/ns/1.0"
ET.register_namespace("", TEI_NS)

# =========================
# DETECTARE LEMĂ IORDAN
# =========================
def is_lemma(line):
    line = line.strip()

    if len(line) < 2:
        return False

    # elimină zgomot OCR
    if re.search(r"\d{2,}", line):
        return False

    # Iordan: inițială mare + rest litere mici
    return bool(re.match(r"^[A-ZĂÂÎȘȚ][a-zăâîșț\- ]+$", line))

# =========================
# CURĂȚARE
# =========================
def clean(line):
    line = line.strip()
    line = re.sub(r"\s+", " ", line)
    return line

# =========================
# PARSARE
# =========================
entries = []
current = None

with open(input_file, "r", encoding="utf-8") as f:

    for line in f:
        line = clean(line)

        if not line:
            continue

        # NOUĂ LEMĂ
        if is_lemma(line):

            if current:
                entries.append(current)

            current = {
                "lemma": line.upper(),
                "defs": []
            }

        else:
            if current:
                current["defs"].append(line)

# adaugă ultima intrare
if current:
    entries.append(current)

# =========================
# TEI OUTPUT
# =========================
root = ET.Element(f"{{{TEI_NS}}}TEI")
text = ET.SubElement(root, f"{{{TEI_NS}}}text")
body = ET.SubElement(text, f"{{{TEI_NS}}}body")

for e in entries:

    entry = ET.SubElement(body, f"{{{TEI_NS}}}entry")

    form = ET.SubElement(entry, f"{{{TEI_NS}}}form")
    orth = ET.SubElement(form, f"{{{TEI_NS}}}orth")
    orth.text = e["lemma"]

    sense = ET.SubElement(entry, f"{{{TEI_NS}}}sense")

    def_text = " ".join(e["defs"])

    d = ET.SubElement(sense, f"{{{TEI_NS}}}def")
    d.text = def_text

    cit = ET.SubElement(sense, f"{{{TEI_NS}}}cit", {"type": "source"})
    bibl = ET.SubElement(cit, f"{{{TEI_NS}}}bibl")
    bibl.text = "Iordan"

ET.ElementTree(root).write(output_file, encoding="utf-8", xml_declaration=True)

print("GATA IORDAN PARSER")
print("Intrări:", len(entries))
print("Output:", output_file)