import xml.etree.ElementTree as ET
from pathlib import Path
import re
from collections import defaultdict

FILE1 = Path(r"C:\Users\User\Desktop\DICTIONAR_UNIFICAT_FINAL_TOTAL.xml")
FILE2 = Path(r"C:\Users\User\Desktop\lexonomy_tei.xml")


# =========================
# CLEAN
# =========================
def clean(word):
    if not word:
        return None
    word = word.strip().lower()
    word = re.sub(r"^[^a-zăâîșț]+|[^a-zăâîșț]+$", "", word)
    if not word:
        return None
    if any(c.isdigit() for c in word):
        return None
    return word


# =========================
# EXTRACT
# =========================
def extract(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    data = defaultdict(list)

    for entry in root.iter("entry"):
        orth = entry.find(".//orth")
        if orth is None or not orth.text:
            continue

        lemma = clean(orth.text)
        if not lemma:
            continue

        for d in entry.iter():
            if d.tag.endswith("def") and d.text:
                data[lemma].append(d.text.strip())

    return data


# =========================
# RUN
# =========================
d1 = extract(FILE1)
d2 = extract(FILE2)

word = "Adăniloaiei"

print("\n=== CUVÂNT:", word, "===\n")

print("--- DICTIONAR 1 ---")
if word in d1:
    for d in d1[word]:
        print("-", d)
else:
    print("NU EXISTA")

print("\n--- DICTIONAR 2 ---")
if word in d2:
    for d in d2[word]:
        print("-", d)
else:
    print("NU EXISTA")


print("\n--- DIN DICTIONAR 1 ---")
for d in d1[word]:
    print("-", d)

print("\n--- DIN DICTIONAR 2 ---")
for d in d2[word]:
    print("-", d)
