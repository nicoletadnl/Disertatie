from lxml import etree
from pathlib import Path

# Căile fișierelor
FILE_IORDAN_TXT = Path(r"C:\Users\User\Desktop\iordan_curatat.txt")
OUTPUT_XML = Path(r"C:\Users\User\Desktop\iordan_formatat.xml")


def transforma_iordan_in_xml():
    # Creăm rădăcina XML
    root = etree.Element("root")

    if FILE_IORDAN_TXT.exists():
        with open(FILE_IORDAN_TXT, "r", encoding="utf-8") as f:
            for line in f:
                if "\t" not in line: continue
                parts = line.split("\t", 1)
                lemma = parts[0].strip()
                def_text = parts[1].strip()

                # Construim structura exact ca în image_668993.png
                entry = etree.SubElement(root, "entry")

                form = etree.SubElement(entry, "form")
                etree.SubElement(form, "orth").text = lemma

                sense = etree.SubElement(entry, "sense")
                etree.SubElement(sense, "def").text = def_text
                etree.SubElement(sense, "bibl").text = "Iordan"

                # Adăugăm blocul external_data
                ext = etree.SubElement(entry, "external_data")
                etree.SubElement(ext, "dex_url").text = f"https://dexonline.ro/definitie/{lemma}"
                etree.SubElement(ext, "clre_url").text = f"https://clre.ro/cautare?q={lemma}"

    # Salvare fișier XML valid
    etree.ElementTree(root).write(str(OUTPUT_XML), pretty_print=True, encoding="utf-8", xml_declaration=True)
    print(f"Transformare reușită! Fișierul XML este aici: {OUTPUT_XML}")


if __name__ == "__main__":
    transforma_iordan_in_xml()