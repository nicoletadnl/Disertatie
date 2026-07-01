import xml.etree.ElementTree as ET

# Fișierul XML de intrare
input_file = r"C:\Users\User\Desktop\iordan_STRUCTURAT.xml"

# Fișierul XML de ieșire
output_file = r"C:\Users\User\Desktop\iordan_STRUCTURAT_cu_sursa.xml"

# Parsează XML-ul
tree = ET.parse(input_file)
root = tree.getroot()

# Textul sursei
source_text = "Dicționar al numelor de familie românești – Iorgu Iordan (1983)"

# Adaugă <source> în fiecare <entry>
for entry in root.iter("entry"):
    # Verifică dacă există deja
    if entry.find("source") is None:
        source = ET.Element("source")
        source.text = source_text
        entry.append(source)

# Salvează noul fișier
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print("Gata!")
print("Fișierul a fost salvat ca:")
print(output_file)