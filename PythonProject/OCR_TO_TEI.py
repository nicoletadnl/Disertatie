import re
from pathlib import Path
from lxml import etree

INPUT = Path(r"C:\Users\User\Desktop\ocr_output.txt")
OUTPUT = Path(r"C:\Users\User\Desktop\lexonomy_tei.xml")

# =========================
# LOAD TEXT
# =========================

raw = INPUT.read_text(encoding="utf-8", errors="ignore")
lines = [l.strip() for l in raw.split("\n")]

# =========================
# 1. FILTER: valid lemma
# =========================

def is_lemma(line: str) -> bool:
    if not line:
        return False

    line = line.strip()

    # elimină zgomot OCR
    if len(line) <= 1:
        return False

    # elimină litere singure (A, B, C...)
    if re.fullmatch(r"[A-ZĂÂÎȘȚ]", line):
        return False

    # elimină numerotări
    if re.fullmatch(r"\d+\.?", line):
        return False

    # elimină cross-references
    if " v. " in line or line.startswith("v."):
        return False

    # trebuie să înceapă cu literă mare
    if not re.match(r"^[A-ZĂÂÎȘȚ]", line):
        return False

    return True


# =========================
# 2. PARSARE OCR → STRUCTURĂ
# =========================

entries = []

current_lemma = None
current_def = []

for line in lines:

    if not line:
        continue

    # START ENTRY
    if is_lemma(line):

        if current_lemma:
            entries.append((current_lemma, " ".join(current_def).strip()))

        parts = line.split(" ", 1)

        current_lemma = parts[0].strip(" ,.;")
        current_def = []

        if len(parts) > 1:
            current_def.append(parts[1])

    else:
        # continuare definiție (IMPORTANT: tot ce NU e lemma)
        if current_lemma:
            current_def.append(line)

# salvare ultimă intrare
if current_lemma:
    entries.append((current_lemma, " ".join(current_def).strip()))


print("Intrări detectate:", len(entries))


# =========================
# 3. TEI GENERATION
# =========================

TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"

root = etree.Element(f"{{{TEI_NS}}}TEI", nsmap={None: TEI_NS})
text_el = etree.SubElement(root, f"{{{TEI_NS}}}text")
body = etree.SubElement(text_el, f"{{{TEI_NS}}}body")

for i, (lemma, definition) in enumerate(entries, 1):

    entry = etree.SubElement(body, f"{{{TEI_NS}}}entry")
    entry.set(f"{{{XML_NS}}}id", f"e{i}")

    form = etree.SubElement(entry, f"{{{TEI_NS}}}form")
    orth = etree.SubElement(form, f"{{{TEI_NS}}}orth")
    orth.text = lemma

    sense = etree.SubElement(entry, f"{{{TEI_NS}}}sense")
    def_el = etree.SubElement(sense, f"{{{TEI_NS}}}def")
    def_el.text = definition

# =========================
# SAVE XML
# =========================

tree = etree.ElementTree(root)
tree.write(
    str(OUTPUT),
    encoding="utf-8",
    xml_declaration=True,
    pretty_print=True
)

print("GATA TEI:", OUTPUT)