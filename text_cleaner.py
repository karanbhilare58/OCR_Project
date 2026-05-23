import re



import re


def normalize_ocr_text(text):

    text = re.sub(
        r'TOTA[\]\|]',
        'TOTAL',
        text
    )

    text = re.sub(
        r'(\d+),(\d{2})(?!\d)',
        r'\1.\2',
        text
    )

    return text

def clean_text(text):

    text = text.upper()

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # fix common OCR mistakes
    text = text.replace("PHOT0", "PHOTO")
    text = text.replace("CANERA", "CAMERA")
    text = text.replace("SUBT0TAL", "SUBTOTAL")

    return text