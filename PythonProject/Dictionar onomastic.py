import os
import re
import io
from pathlib import Path
from collections import defaultdict

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from lxml import etree
from unidecode import unidecode

# ============================================
# CONFIG
# ============================================

# Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Folder cu PDF-urile scanate
INPUT_FOLDER = Path(r"C:\Users\User\Desktop\dictionarr")

# Fișierul XML rezultat
OUTPUT_FILE = Path(
    r"C:\Users\User\Desktop\dictionarr_output\lexonomy_tei.xml"
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Linkuri externe
DEFAULT_LINKS = [
    "https://dexonline.ro/definitie/{lemma}",
]

# ============================================
# STORAGE
# ============================================

entries = defaultdict(lambda: {
    "lemma": "",
    "forms": set(),
    "senses": [],
    "sources": set(),
    "links": set()
})

# ============================================
# OCR PDF CU PyMuPDF
# ============================================

def ocr_pdf(pdf_path: Path) -> str:
    print(f"  → Deschid PDF-ul cu PyMuPDF...")

    try:
        doc = fitz.open(str(pdf_path))
    except Exception as e:
        print(f"  ❌ Nu pot deschide PDF-ul: {e}")
        return ""

    text_parts = []

    total_pages = len(doc)

    print(f"  → Total pagini: {total_pages}")

    for page_num in range(total_pages):
        print(f"  → OCR pagina {page_num + 1}/{total_pages}")

        try:
            page = doc[page_num]

            # Randare pagină la rezoluție mare
            pix = page.get_pixmap(dpi=300)

            # Conversie în imagine PIL
            img = Image.open(io.BytesIO(pix.tobytes("png")))

            # OCR
            text = pytesseract.image_to_string(
                img,
                lang="ron",
                config="--oem 1 --psm 4"
            )

            text_parts.append(text)

        except Exception as e:
            print(f"    ❌ Eroare pagina {page_num + 1}: {e}")

    return "\n".join(text_parts)

# ============================================
# PARSER
# ============================================

ENTRY_PATTERN = re.compile(
    r'^\s*([A-ZĂÂÎȘȚ][A-ZĂÂÎȘȚa-zăâîșț\-]+)\s+(.+?)(?=\n[A-ZĂÂÎȘȚ][A-ZĂÂÎȘȚa-zăâîșț\-]+\s|\Z)',
    re.MULTILINE | re.DOTALL
)

FORM_PATTERN = re.compile(
    r'([A-ZĂÂÎȘȚ][a-zăâîșț]+)\s*\([^)]+\)'
)

def clean_text(text: str) -> str:
    text = text.replace('\u0000', '')
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    return text

def parse_onomastic(text: str, source: str):
    text = clean_text(text)

    results = []

    for match in ENTRY_PATTERN.finditer(text):

        lemma = match.group(1).strip()
        definition = match.group(2).strip()

        definition = re.sub(r'\s+', ' ', definition)

        # Filtrări
        if len(lemma) < 2:
            continue

        if len(definition) < 5:
            continue

        if any(c.isdigit() for c in lemma):
            continue

        forms = {lemma}

        for form_match in FORM_PATTERN.finditer(definition):
            forms.add(form_match.group(1))

        results.append({
            "lemma": lemma,
            "forms": forms,
            "definition": definition,
            "source": source
        })

    return results

# ============================================
# MERGE
# ============================================

def merge_entry(key: str, item: dict):

    entry = entries[key]

    if not entry["lemma"]:
        entry["lemma"] = item["lemma"]

    entry["forms"].update(item["forms"])

    entry["sources"].add(item["source"])

    existing_defs = [s["def"] for s in entry["senses"]]

    if item["definition"] not in existing_defs:
        entry["senses"].append({
            "def": item["definition"],
            "source": item["source"]
        })

    for link_template in DEFAULT_LINKS:
        entry["links"].add(
            link_template.format(lemma=item["lemma"])
        )

# ============================================
# TEI GENERATION
# ============================================

TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"

NSMAP = {
    None: TEI_NS
}

def build_tei():

    root = etree.Element(
        f"{{{TEI_NS}}}TEI",
        nsmap=NSMAP
    )

    # ========================================
    # HEADER
    # ========================================

    header = etree.SubElement(
        root,
        f"{{{TEI_NS}}}teiHeader"
    )

    file_desc = etree.SubElement(
        header,
        f"{{{TEI_NS}}}fileDesc"
    )

    title_stmt = etree.SubElement(
        file_desc,
        f"{{{TEI_NS}}}titleStmt"
    )

    title = etree.SubElement(
        title_stmt,
        f"{{{TEI_NS}}}title"
    )

    title.text = "Dicționar Onomastic Combinat"

    publication_stmt = etree.SubElement(
        file_desc,
        f"{{{TEI_NS}}}publicationStmt"
    )

    p_pub = etree.SubElement(
        publication_stmt,
        f"{{{TEI_NS}}}p"
    )

    p_pub.text = "Generat automat din PDF-uri scanate"

    source_desc = etree.SubElement(
        file_desc,
        f"{{{TEI_NS}}}sourceDesc"
    )

    p_source = etree.SubElement(
        source_desc,
        f"{{{TEI_NS}}}p"
    )

    p_source.text = "Dicționare onomastice scanate"

    # ========================================
    # TEXT
    # ========================================

    text_el = etree.SubElement(
        root,
        f"{{{TEI_NS}}}text"
    )

    body = etree.SubElement(
        text_el,
        f"{{{TEI_NS}}}body"
    )

    # ========================================
    # ENTRIES
    # ========================================

    for idx, (key, data) in enumerate(
        sorted(entries.items()),
        start=1
    ):

        entry_el = etree.SubElement(
            body,
            f"{{{TEI_NS}}}entry"
        )

        entry_el.set(
            f"{{{XML_NS}}}id",
            f"e{idx}"
        )

        # FORM
        form_el = etree.SubElement(
            entry_el,
            f"{{{TEI_NS}}}form"
        )

        form_el.set("type", "lemma")

        for form_text in sorted(data["forms"]):

            orth = etree.SubElement(
                form_el,
                f"{{{TEI_NS}}}orth"
            )

            orth.text = form_text

        # SENSES
        for i, sense_data in enumerate(
            data["senses"],
            start=1
        ):

            sense = etree.SubElement(
                entry_el,
                f"{{{TEI_NS}}}sense"
            )

            sense.set("n", str(i))

            def_el = etree.SubElement(
                sense,
                f"{{{TEI_NS}}}def"
            )

            def_el.text = sense_data["def"]

            bibl = etree.SubElement(
                sense,
                f"{{{TEI_NS}}}bibl"
            )

            bibl.text = sense_data["source"]

        # LINKS
        for link_url in sorted(data["links"]):

            ref = etree.SubElement(
                entry_el,
                f"{{{TEI_NS}}}ref"
            )

            ref.set("target", link_url)

            ref.text = link_url.split("/")[-1]

        # NOTE
        if data["sources"]:

            note = etree.SubElement(
                entry_el,
                f"{{{TEI_NS}}}note"
            )

            note.set("type", "sources")

            note.text = ", ".join(
                sorted(data["sources"])
            )

    return root

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("PDF SCANAT → TEI XML PENTRU LEXONOMY")
    print("=" * 60 + "\n")

    # Verificare folder input
    if not INPUT_FOLDER.exists():

        print(f"❌ Folderul nu există:")
        print(INPUT_FOLDER)

        exit(1)

    # PDF-uri
    pdf_files = list(INPUT_FOLDER.glob("*.pdf"))

    print(f"Găsite {len(pdf_files)} fișiere PDF\n")

    if not pdf_files:
        print("❌ Nu există PDF-uri.")
        exit(1)

    # Procesare PDF-uri
    for pdf_path in pdf_files:

        print(f"\n📄 {pdf_path.name}")

        text = ocr_pdf(pdf_path)

        if not text.strip():

            print("   ⚠️ Nu s-a extras text.")
            continue

        parsed = parse_onomastic(
            text,
            source=pdf_path.name
        )

        print(f"   → {len(parsed)} intrări extrase")

        for item in parsed:

            key = unidecode(
                item["lemma"].lower()
            )

            merge_entry(key, item)

    # ========================================
    # GENERARE XML
    # ========================================

    print("\n" + "=" * 60)
    print("GENERARE TEI XML")
    print("=" * 60)

    if not entries:

        print("\n❌ Nu s-au extras intrări valide.")
        exit(1)

    tei_root = build_tei()

    tree = etree.ElementTree(tei_root)

    tree.write(
        str(OUTPUT_FILE),
        pretty_print=True,
        encoding="utf-8",
        xml_declaration=True
    )

    print(f"\n✅ Intrări totale: {len(entries)}")
    print(f"📁 XML salvat în:")
    print(OUTPUT_FILE)

    print("\n✅ Gata.")