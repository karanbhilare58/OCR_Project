import re

from services.nlp_service import extract_entities


def extract_amount(keyword, text):

    pattern = rf"{keyword}\s*[:\-]?\s*\$?([0-9,]+\.\d{{2}})"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return None


def parse_receipt(text):

    entities = extract_entities(text)

    subtotal = extract_amount("subtotal", text)

    tax = extract_amount("tax", text)

    total = extract_amount("total", text)

    date_match = re.search(
        r"\d{2}/\d{2}/\d{2,4}",
        text
    )

    date = date_match.group(0) if date_match else None

    money_entities = entities["money"]

    if not total and money_entities:

        total = money_entities[-1]

    return {

        "date": date,

        "subtotal": subtotal,

        "tax": tax,

        "total": total,

        "money_entities": money_entities
    }