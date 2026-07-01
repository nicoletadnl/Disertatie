# ... (restul importurilor)

# Modificăm funcția de restructurare pentru a păstra sursa corectă
def restructureaza_corect():
    # ... (citirea fișierului)

    # Presupunem că structura din fișierul de intrare are informația sursei
    # Dacă nu are, trebuie să tratăm fragmentele separat
    for entry in tree.xpath('//entry'):
        # Aici extragem și sursa (bibl) din fișierul original, dacă este disponibilă
        bibl_original = entry.xpath('.//bibl')
        nume_sursa = bibl_original[0].text if bibl_original else "Iordan"

        def_text = "".join([d.text for d in entry.xpath('.//def') if d.text])

        # ... (regex-ul de mai sus pentru separare)

        for i in range(1, len(parti), 2):
            # ... (logica de creare a intrării)

            new_entry = etree.SubElement(root_out, "entry")
            etree.SubElement(new_entry, "orth").text = lema
            sense = etree.SubElement(new_entry, "sense")

            # Aici scriem sursa corectă detectată anterior
            etree.SubElement(sense, "bibl").text = nume_sursa

            etree.SubElement(sense, "def").text = continut.strip()