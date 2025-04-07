import random
import os
import qrcode
from qrcode.image.svg import SvgImage
import zipfile
import logging
import shutil

# Setup logger
logger = logging.getLogger("qr_generator")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("generator.log")
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

BASE_DIR = "output"
QR_DIR = os.path.join(BASE_DIR, "qrcodes")
TEXT_FILE = os.path.join(BASE_DIR, "new_codes.txt")
ZIP_FILE = os.path.join(BASE_DIR, "qr_codes.zip")

os.makedirs(QR_DIR, exist_ok=True)

def generate_checksummed_code():
    base = [random.randint(0, 9) for _ in range(14)]
    checksum = sum((i + 1) * num for i, num in enumerate(base)) % 10
    code = "".join(map(str, base)) + str(checksum)
    logger.info(f"Generated code: {code}")
    return code

def validate_code(code):
    if not code.isdigit() or len(code) != 15:
        return False
    base_digits = list(map(int, code[:14]))
    checksum_digit = int(code[-1])
    checksum = sum((i + 1) * num for i, num in enumerate(base_digits)) % 10
    return checksum == checksum_digit

def generate_unique_codes(n):
    codes = set()
    while len(codes) < n:
        codes.add(generate_checksummed_code())
    return list(codes)

def generate_qr_images(codes):
    for code in codes:
        img = qrcode.make(code, image_factory=SvgImage)
        img.save(os.path.join(QR_DIR, f"{code}.svg"))
        logger.info(f"Saved QR code for: {code}")

def save_as_zip(codes):
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)
    os.makedirs(QR_DIR, exist_ok=True)

    with open(TEXT_FILE, "w") as f:
        for c in codes:
            f.write(c + "\n")
    logger.info(f"Saved text file with {len(codes)} codes")

    generate_qr_images(codes)

    with zipfile.ZipFile(ZIP_FILE, "w") as zipf:
        zipf.write(TEXT_FILE, arcname="new_codes.txt")
        for filename in os.listdir(QR_DIR):
            file_path = os.path.join(QR_DIR, filename)
            zipf.write(file_path, arcname=f"qrcodes/{filename}")
    logger.info(f"ZIP archive created at {ZIP_FILE}")
    return ZIP_FILE