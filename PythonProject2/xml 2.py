import re
import xml.etree.ElementTree as ET

# =========================
# CONFIG
# =========================
INPUT_IORDAN = r"C:\Users\User\Desktop\disertatie\output\iordan_raw.txt"
INPUT_CONST = r"C:\Users\User\Desktop\disertatie\output\constantinescu_raw.txt"

OUT_IORDAN_XML = r"C:\Users\User\Desktop\disertatie\output\iordan.xml"
OUT_CONST_XML = r"C:\Users\User\Desktop\disertatie\output\constantinescu.xml"


# =========================
# CURĂȚARE OCR
# =========================
def clean_lines(lines):
    cleaned = []

    for line in lines:
        line = line.strip()

        # elimină zgomot
        if not line:
            continue

        if re.fullmatch(r"[a-zA-Z0-9\.\,\)\(;]+", line.lower()):
            continue

        # trebuie să conțină litere
        if not re.search(r"[A-Za-zĂÂÎȘȚăâîșț]", line):
            continue

        # elimină linii gen a., a0.);
        if len(line) < 3:
            continue

        cleaned.append(line)

    return cleaned


# =========================
# DETECTARE LEMĂ
# =========================
def is_lemma(line):
    line = line.strip()

    # începe cu literă mare (regula Iordan/Constantinescu)
    if not re.match(r"^[A-ZĂÂÎȘȚ]", line):
        return False

    # trebuie să aibă litere reale
    if len(re.findall(r"[A-Za-zĂÂÎȘȚăâîșț]", line)) < 3:
        return False

    return True


# =========================
# PARSARE OCR → STRUCTURĂ
# =========================
def parse_to_entries(lines, source_name):
    entries = []

    current = None

    for line in lines:

        if is_lemma(line):
            if current:
                entries.append(current)

            current = {
                "lemma": line.strip(),
                "def": "",
                "source": source_name
            }
        else:
            if current:
                current["def"] += " " + line.strip()

    if current:
        entries.append(current)

    return entries


# =========================
# EXPORT XML TEI
# =========================
def to_xml(entries, output_file, source_name):

    TEI = "{http://www.tei-c.org/ns/1.0}"

    root = ET.Element(f"{TEI}TEI")
    text = ET.SubElement(root, f"{TEI}text")
    body = ET.SubElement(text, f"{TEI}body")

    for e in entries:

        entry = ET.SubElement(body, f"{TEI}entry")

        form = ET.SubElement(entry, f"{TEI}form")
        orth = ET.SubElement(form, f"{TEI}orth")
        orth.text = e["lemma"]

        sense = ET.SubElement(entry, f"{TEI}sense")

        d = ET.SubElement(sense, f"{TEI}def")
        d.text = e["def"].strip()

        cit = ET.SubElement(sense, f"{TEI}cit", {"type": "source"})
        bibl = ET.SubElement(cit, f"{TEI}bibl")
        bibl.text = source_name

    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


# =========================
# PIPELINE IORDAN
# =========================
with open(INPUT_IORDAN, "r", encoding="utf-8") as f:
    lines = clean_lines(f.readlines())

entries_iordan = parse_to_entries(lines, "Iordan")
to_xml(entries_iordan, OUT_IORDAN_XML, "Iordan")

print("IORDAN DONE:", len(entries_iordan))


# =========================
# PIPELINE CONSTANTINESCU
# =========================
with open(INPUT_CONST, "r", encoding="utf-8") as f:
    lines = clean_lines(f.readlines())

entries_const = parse_to_entries(lines, "Constantinescu")
to_xml(entries_const, OUT_CONST_XML, "Constantinescu")

print("CONSTANTINESCU DONE:", len(entries_const))
