import re

from services.nlp_service import extract_entities

def normalize_amount(value):

    if value is None:
        return None

    return value.replace(",", "").strip()


def extract_amount(keyword, text):

    pattern = rf"{keyword}.*?\$?([0-9,]+\.\d{{2}})"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return None

def extract_total_smart(text):

    matches = re.findall(
        r'([0-9,]+\.\d{2})',
        text
    )

    if not matches:
        return None

    amounts = []

    for value in matches:

        try:
            cleaned = float(
                value.replace(",", "")
            )

            amounts.append((cleaned, value))

        except:
            continue

    if not amounts:
        return None

    amounts.sort(reverse=True)

    return amounts[0][1]


def parse_receipt(text):

    entities = extract_entities(text)

    subtotal = extract_amount("subtotal", text)

    tax = extract_amount("tax", text)

    total_patterns = [

    r"total\s*payment",
    r"total\s*order",
    r"\btotal\b"
]

    total = None

    for pattern in total_patterns:

        total = extract_amount(pattern, text)

        if total:
            break

    date_match = re.search(
        r"\d{2}/\d{2}/\d{2,4}",
        text
    )

    date = date_match.group(0) if date_match else None

    money_entities = entities["money"]

    if not total:
        total = extract_total_smart(text)

    subtotal = normalize_amount(subtotal)

    tax = normalize_amount(tax)

    total = normalize_amount(total)

    return {

        "date": date,

        "subtotal": subtotal,

        "tax": tax,

        "total": total,

        "money_entities": money_entities
    }