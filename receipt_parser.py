import re
from services.nlp_service import extract_entities

def normalize_amount(value):
    if value is None:
        return None
    
    value = value.strip()
    
    # OCR FIX: Handle spaces OR underscores acting as decimal points before the last two digits
    value = re.sub(r'[\s_]+(\d{2})$', r'.\1', value)
    
    # Clean up commas, internal spaces, and rogue underscores
    value = value.replace(",", "").replace(" ", "").replace("_", "")

    return value

def extract_total_smart(text):
    matches = re.findall(r'([0-9,]+\.\d{2})', text)
    if not matches:
        return None

    amounts = []
    for value in matches:
        try:
            cleaned = float(value.replace(",", ""))
            amounts.append((cleaned, value))
        except:
            continue

    if not amounts:
        return None

    amounts.sort(reverse=True)
    return amounts[0][1]

def parse_receipt(text):
    entities = extract_entities(text)
    
    clean_text = re.sub(r"\([\d\s\.%]+\)", "", text)

    amount_pattern = r"([0-9,\s]+[\.\s_][0-9]{2})"

    sub_match = re.search(r"\bSUBTOTAL\b.*?" + amount_pattern, clean_text, re.IGNORECASE)
    subtotal = normalize_amount(sub_match.group(1)) if sub_match else None

    tax_matches = list(re.finditer(r"\bTAX\b.*?" + amount_pattern, clean_text, re.IGNORECASE))
    tax = normalize_amount(tax_matches[-1].group(1)) if tax_matches else None

    total_match = re.search(r"\bTOTAL\b.*?" + amount_pattern, clean_text, re.IGNORECASE)
    total = normalize_amount(total_match.group(1)) if total_match else None

    date_match = re.search(r"\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{2,4}", text)
    date = date_match.group(0) if date_match else None

    if subtotal and tax:
        try:
            sub_val = float(subtotal)
            tax_val = float(tax)
            calc_total = sub_val + tax_val
            
            # If we didn't find a total, or the total the OCR found is clearly wrong 
            # (e.g., more than a $1.00 difference), trust the math instead of the OCR.
            if not total or abs(float(total) - calc_total) > 1.0:
                total = f"{calc_total:.2f}"
        except ValueError:
            pass 
            
    
    if not total:
        total = normalize_amount(extract_total_smart(text))

    
    return {
        "date": date,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "money_entities": entities.get("money", [])
    }