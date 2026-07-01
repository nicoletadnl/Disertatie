import os
import xml.etree.ElementTree as ET

# =========================
# OUTPUT PATH SIGUR
# =========================
output_path = os.path.join(
    os.path.expanduser("~"),
    "Desktop",
    "disertatie",
    "output",
    "dictionar_iulie.xml"
)

# =========================
# CREARE FOLDER DACĂ NU EXISTĂ
# =========================
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# =========================
# AICI ESTE ROOT-UL TĂU XML
# (presupun că deja ai construit "root")
# =========================
# tree = ET.ElementTree(root)

# =========================
# SALVARE XML
# =========================
tree.write(output_path, encoding="utf-8", xml_declaration=True)

# =========================
# VERIFICARE FINALĂ
# =========================
print("✔ DICTIONAR SALVAT LA:")
print(output_path)

if os.path.exists(output_path):
    print("✔ FIȘIER EXISTĂ (OK)")
else:
    print("❌ EROARE: fișierul nu s-a creat")