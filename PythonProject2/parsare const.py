import re
import xml.etree.ElementTree as ET

input_file = r"C:\Users\User\Desktop\disertatie\output\constantinescu_raw.txt"
output_file = r"C:\Users\User\Desktop\disertatie\output\constantinescu.xml"

TEI_NS = "http://www.tei-c.org/ns/1.0"
ET.register_namespace("", TEI_NS)

# =========================
# CURĂȚARE
# =========================
def clean(line):
    line = line.strip()
    line = re.sub(r"\s+", " ", line)
    return line

# =========================
# DETECTARE ZGOMOT OCR
# =========================
def is_noise(line):
    if len(line) < 2:
        return True
    if re.search(r"www|http|dacaromanica|pagina|\d{3,}", line.lower()):
        return True
    if line in ["A", "B", "C", "D", "E"]:
        return True
    return False

# =========================
# DETECTARE LEMĂ REALĂ
# =========================
def is_lemma(line):
    line = line.strip()

    if is_noise(line):
        return False

    # CASE 1: ABEL, ACACHIE (majuscule)
    if re.match(r"^[A-ZĂÂÎȘȚ]{2,}", line):
        return True

    # CASE 2: Absalom v. Avesalom
    if " v. " in line:
        return True

    # CASE 3: intrare tip „Ababei < Baba”
    if "<" in line:
        return True

    return False

# =========================
# PARSARE
# =========================
entries = []

with open(input_file, "r", encoding="utf-8") as f:
    lines = [clean(l) for l in f if clean(l)]

current = None

for line in lines:

    if is_lemma(line):

        if current:
            entries.append(current)

        # extragere lemă
        lemma = re.split(r"[<:]", line)[0]
        lemma = re.split(r" v\. ", lemma)[0]
        lemma = lemma.strip()

        current = {
            "lemma": lemma,
            "def": []
        }

        # dacă are definiție pe aceeași linie
        rest = line[len(lemma):].strip(" <.:")
        if rest:
            current["def"].append(rest)

    else:
        if current:
            current["def"].append(line)

if current:
    entries.append(current)

# =========================
# FILTRARE FINALĂ
# =========================
final_entries = []

for e in entries:

    lemma = e["lemma"].strip()
    definition = " ".join(e["def"]).strip()

    if len(lemma) < 2:
        continue
    if len(definition) < 3:
        continue

    final_entries.append({
        "lemma": lemma,
        "def": definition
    })

# =========================
# XML TEI
# =========================
root = ET.Element(f"{{{TEI_NS}}}TEI")
text_el = ET.SubElement(root, f"{{{TEI_NS}}}text")
body = ET.SubElement(text_el, f"{{{TEI_NS}}}body")

for e in final_entries:

    entry = ET.SubElement(body, f"{{{TEI_NS}}}entry")

    form = ET.SubElement(entry, f"{{{TEI_NS}}}form")
    orth = ET.SubElement(form, f"{{{TEI_NS}}}orth")
    orth.text = e["lemma"]

    sense = ET.SubElement(entry, f"{{{TEI_NS}}}sense")

    d = ET.SubElement(sense, f"{{{TEI_NS}}}def")
    d.text = e["def"]

    cit = ET.SubElement(sense, f"{{{TEI_NS}}}cit", {"type": "source"})
    bibl = ET.SubElement(cit, f"{{{TEI_NS}}}bibl")
    bibl.text = "Constantinescu"

ET.ElementTree(root).write(output_file, encoding="utf-8", xml_declaration=True)

print("GATA CONSTANTINESCU v3 REAL")
print("Intrări:", len(final_entries))
print("Output:", output_file)