import re
from pathlib import Path
from lxml import etree

# ==========================================
# FILES
# ==========================================

INPUT = Path(r"C:\Users\User\Desktop\ocr_output.txt")
OUTPUT = Path(r"C:\Users\User\Desktop\lexonomy_tei.xml")

# ==========================================
# LOAD OCR TEXT
# ==========================================

raw = INPUT.read_text(encoding="utf-8", errors="ignore")

# normalizare
raw = raw.replace("\r", "")
raw = re.sub(r"[ \t]+", " ", raw)

lines = raw.split("\n")

# ==========================================
# BAD OCR WORDS
# ==========================================

BAD_WORDS = {
    "A", "B", "C", "D",
    "AI", "AL", "ALE",
    "A1", "A0", "A2",
    "II", "III", "IV",
    "V", "VI", "VII"
}

# ==========================================
# DETECT LEMMA
# ==========================================

def is_lemma(line):

    line = line.strip()

    if not line:
        return False

    # prea scurt
    if len(line) < 3:
        return False

    # numere
    if re.fullmatch(r"\d+\.?", line):
        return False

    # OCR garbage
    if line in BAD_WORDS:
        return False

    # trebuie să înceapă cu MAJUSCULE
    if not re.match(r"^[A-ZĂÂÎȘȚ][A-ZĂÂÎȘȚ\-]+", line):
        return False

    return True

# ==========================================
# PARSARE
# ==========================================

entries = []

current_lemma = None
current_definition = []

for line in lines:

    line = line.strip()

    if not line:
        continue

    # ======================================
    # ENTRY NOU
    # ======================================

    if is_lemma(line):

        # salvare entry anterior
        if current_lemma:

            definition = " ".join(current_definition).strip()

            # curățare spații
            definition = re.sub(r"\s+", " ", definition)

            # elimină definiții goale
            if len(definition) > 2:

                # evită duplicate consecutive
                if not (
                    entries and
                    entries[-1]["lemma"] == current_lemma
                ):

                    entries.append({
                        "lemma": current_lemma,
                        "definition": definition
                    })

        # ==================================
        # EXTRAGE LEMMA
        # ==================================

        m = re.match(r"^([A-ZĂÂÎȘȚ\-]+)", line)

        lemma = m.group(1).strip()

        lemma = lemma.replace(",", "")
        lemma = lemma.replace(".", "")

        # restul liniei = definiție
        definition_start = line[m.end():].strip(" ,.;:")

        # elimină lemma repetată din definiție
        if definition_start.startswith(lemma):
            definition_start = definition_start[len(lemma):].strip()

        current_lemma = lemma
        current_definition = []

        if definition_start:
            current_definition.append(definition_start)

    # ======================================
    # CONTINUARE DEFINIȚIE
    # ======================================

    else:

        if current_lemma:
            current_definition.append(line)

# ==========================================
# ULTIMUL ENTRY
# ==========================================

if current_lemma:

    definition = " ".join(current_definition).strip()
    definition = re.sub(r"\s+", " ", definition)

    if len(definition) > 2:

        if not (
            entries and
            entries[-1]["lemma"] == current_lemma
        ):

            entries.append({
                "lemma": current_lemma,
                "definition": definition
            })

# ==========================================
# ELIMINARE DUPLICATE GLOBALE
# ==========================================

unique_entries = []
seen = set()

for item in entries:

    key = item["lemma"]

    if key not in seen:
        unique_entries.append(item)
        seen.add(key)

entries = unique_entries

print("Intrări finale:", len(entries))

# ==========================================
# TEI XML
# ==========================================

TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"

root = etree.Element(
    f"{{{TEI_NS}}}TEI",
    nsmap={None: TEI_NS}
)

text_el = etree.SubElement(
    root,
    f"{{{TEI_NS}}}text"
)

body = etree.SubElement(
    text_el,
    f"{{{TEI_NS}}}body"
)

# ==========================================
# GENERARE ENTRIES
# ==========================================

for i, item in enumerate(entries, 1):

    entry = etree.SubElement(
        body,
        f"{{{TEI_NS}}}entry"
    )

    entry.set(
        f"{{{XML_NS}}}id",
        f"e{i}"
    )

    # FORM
    form = etree.SubElement(
        entry,
        f"{{{TEI_NS}}}form"
    )

    orth = etree.SubElement(
        form,
        f"{{{TEI_NS}}}orth"
    )

    orth.text = item["lemma"]

    # SENSE
    sense = etree.SubElement(
        entry,
        f"{{{TEI_NS}}}sense"
    )

    def_el = etree.SubElement(
        sense,
        f"{{{TEI_NS}}}def"
    )

    def_el.text = item["definition"]

# ==========================================
# SAVE XML
# ==========================================

tree = etree.ElementTree(root)

tree.write(
    str(OUTPUT),
    pretty_print=True,
    encoding="utf-8",
    xml_declaration=True
)

print("GATA TEI:")
print(OUTPUT)