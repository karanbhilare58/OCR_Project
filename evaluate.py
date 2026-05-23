import json
import os

from services.ai_ocr_service import process_receipt_easyocr


GROUND_TRUTH_PATH = "data/ground_truth.json"

RECEIPT_FOLDER = "data/receipts"


with open(GROUND_TRUTH_PATH, "r") as file:

    ground_truth = json.load(file)


total_fields = 0
correct_fields = 0


for filename, expected in ground_truth.items():

    filepath = os.path.join(RECEIPT_FOLDER, filename)

    print("\n========================")
    print(f"Evaluating: {filename}")
    print("========================")

    result = process_receipt_easyocr(filepath)

    extracted = result["fields"]

    for field, expected_value in expected.items():

        total_fields += 1

        extracted_value = extracted.get(field)

        if str(extracted_value) == str(expected_value):

            correct_fields += 1

            print(f"[✓] {field}")
            print(f"Expected: {expected_value}")
            print(f"Extracted: {extracted_value}")

        else:

            print(f"[✗] {field}")
            print(f"Expected: {expected_value}")
            print(f"Extracted: {extracted_value}")


accuracy = (correct_fields / total_fields) * 100


print("\n========================")
print("FINAL RESULTS")
print("========================")

print(f"Correct Fields: {correct_fields}")
print(f"Total Fields: {total_fields}")
print(f"Accuracy: {accuracy:.2f}%")