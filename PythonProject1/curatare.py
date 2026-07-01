import re


def curata_text(cale_fisier):
    with open(cale_fisier, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Eliminăm linii care par "zgomot" sau caractere unice ciudate
    # Exemplu: eliminăm linii foarte scurte care sunt doar resturi de OCR
    linii = text.split('\n')
    text_curat = []

    for linie in linii:
        # Eliminăm caracterele de tip 'A' urmat de un caracter neobișnuit la început de linie
        linie = re.sub(r'^A[a-z]{1,2}\s', '', linie)

        # Eliminăm secvențe de caractere care par erori de scanare
        linie = linie.replace(" <.", "<")

        if len(linie.strip()) > 3:  # Păstrăm doar linii cu conținut real
            text_curat.append(linie)

    return "\n".join(text_curat)


# Aplicăm curățarea
text_final = curata_text(r"C:\Users\User\Desktop\iordan_ocr_imagini.txt")

# Salvăm rezultatul
with open(r"C:\Users\User\Desktop\iordan_curatat.txt", "w", encoding="utf-8") as f:
    f.write(text_final)

print("Curățarea a fost finalizată! Verifică iordan_curatat.txt de pe Desktop.")