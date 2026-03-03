import re

def parse_receipt(text):

    result = {}

    # Order number
    order_match = re.search(r'Order[:\s]+(\d+)', text, re.IGNORECASE)
    if order_match:
        result["order_number"] = order_match.group(1)

    # Date
    date_match = re.search(r'\d{2}/\d{2}/\d{2}', text)
    if date_match:
        result["date"] = date_match.group()

    # Subtotal
    subtotal_match = re.search(r'SUBTOTAL\s+([\d,]+\.\d{2})', text, re.IGNORECASE)
    if subtotal_match:
        result["subtotal"] = float(subtotal_match.group(1).replace(",", ""))

    # Tax
    tax_match = re.search(r'Tax[:\s]+([\d,]+\.\d{2})', text, re.IGNORECASE)
    if tax_match:
        result["tax"] = float(tax_match.group(1).replace(",", ""))

    # Total
    total_match = re.search(r'Total.*?([\d,]+\.\d{2})', text, re.IGNORECASE)
    if total_match:
        result["total"] = float(total_match.group(1).replace(",", ""))

    return result