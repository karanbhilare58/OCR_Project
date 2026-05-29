import re



import re


def normalize_ocr_text(text):

    text = text.upper()

    text = text.replace("TOTA]", "TOTAL")
    text = text.replace("{", "")
    text = text.replace("}", "")

    # Fix OCR spaces around decimals
    text = re.sub(
        r'(\d)\s*\.\s*(\d)',
        r'\1.\2',
        text
    )

    # Fix OCR spaces after commas
    text = re.sub(
        r'(\d),\s+(\d)',
        r'\1,\2',
        text
    )

    # Remove duplicate spaces
    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    return text.strip()

def clean_text(text):

    text = text.upper()

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # fix common OCR mistakes
    text = text.replace("PHOT0", "PHOTO")
    text = text.replace("CANERA", "CAMERA")
    text = text.replace("SUBT0TAL", "SUBTOTAL")

    return text