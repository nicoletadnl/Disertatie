import re
import xml.etree.ElementTree as ET


def valid_lemma(lemma):
    if not lemma:
        return False

    lemma = lemma.strip()

    # 1. Elimină lemele prea scurte (sub 2 litere - excepție pentru abrevieri?)
    if len(lemma) < 2:
        return False

    # 2. Elimină lemele care conțin cifre (OCR-ul confundă des 'l' cu '1', 'o' cu '0')
    if re.search(r"\d", lemma):
        return False

    # 3. Verifică dacă conține cel puțin o literă (excludem punctuația pură)
    if not re.search(r"[a-zăâîșțA-ZĂÂÎȘȚ]", lemma):
        return False

    # 4. Verifică dacă este "zgomot" (prea multe simboluri vs litere)
    # Dacă lungimea simbolurilor speciale > 50% din lungimea totală, ignorăm
    symbols = re.findall(r"[^\w\s]", lemma)
    if len(symbols) > len(lemma) / 2:
        return False

    return True


def extract_with_defs(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        results = []

        for entry in root.findall(".//entry"):
            orth = entry.find(".//orth")
            # Folosim .itertext() pentru a prinde tot textul, chiar dacă are tag-uri interne
            defi = entry.find(".//def")

            if orth is None or orth.text is None:
                continue

            lemma = orth.text.strip()

            if not valid_lemma(lemma):
                continue

            definition = "".join(defi.itertext()).strip() if defi is not None else ""
            results.append((lemma, definition))

        return results
    except Exception as e:
        print(f"Eroare la procesarea XML: {e}")
        return []