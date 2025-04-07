import random
import os
import qrcode
import zipfile

BASE_DIR = "output"
SVG_DIR = os.path.join(BASE_DIR, "qrcodes")
TXT_FILE = os.path.join(BASE_DIR, "new_codes.txt")
ZIP_FILE = os.path.join(BASE_DIR, "codigos_qr.zip")

os.makedirs(SVG_DIR, exist_ok=True)

def gerar_codigo_verificavel():
    base = [random.randint(0, 9) for _ in range(7)]
    soma = sum((i + 1) * num for i, num in enumerate(base))
    verificador = soma % 10
    return "".join(map(str, base)) + str(verificador)

def validar_codigo(codigo):
    if not codigo.isdigit() or len(codigo) != 8:
        return False
    base = list(map(int, codigo[:7]))
    verificador = int(codigo[-1])
    soma = sum((i + 1) * num for i, num in enumerate(base))
    return soma % 10 == verificador

def gerar_codigos_unicos(n):
    codigos = set()
    while len(codigos) < n:
        codigos.add(gerar_codigo_verificavel())
    return list(codigos)

def gerar_qr_codes(codigos):
    for codigo in codigos:
        img = qrcode.make(codigo)
        img.save(os.path.join(SVG_DIR, f"{codigo}.png"))

def salvar_em_zip(codigos):
    with open(TXT_FILE, "w") as f:
        for c in codigos:
            f.write(c + "\n")
    gerar_qr_codes(codigos)

    with zipfile.ZipFile(ZIP_FILE, "w") as zipf:
        zipf.write(TXT_FILE, arcname="new_codes.txt")
        for filename in os.listdir(SVG_DIR):
            zipf.write(os.path.join(SVG_DIR, filename), arcname=f"qrcodes/{filename}")
    return ZIP_FILE