import re

def clean_text(text):

    text = text.upper()

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # fix common OCR mistakes
    text = text.replace("PHOT0", "PHOTO")
    text = text.replace("CANERA", "CAMERA")
    text = text.replace("SUBT0TAL", "SUBTOTAL")

    return text