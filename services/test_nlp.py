from services.nlp_service import extract_entities


text = """
Subtotal $3899.00
Tax $341.16
Total $4240.16
Date 07/09/20
"""


entities = extract_entities(text)

print(entities)