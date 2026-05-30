import json
import os
import csv

from services.ai_ocr_service import process_receipt_easyocr

GROUND_TRUTH_PATH = "data/ground_truth.json"
RECEIPT_FOLDER = "data/receipts_test"

with open(GROUND_TRUTH_PATH, "r") as file:
    ground_truth = json.load(file)

report_rows = []
total_fields = 0
correct_fields = 0

# Step 3: Initialize per-field counters
field_stats = {
    "date": {"correct": 0, "total": 0},
    "subtotal": {"correct": 0, "total": 0},
    "tax": {"correct": 0, "total": 0},
    "total": {"correct": 0, "total": 0}
}

for filename, expected in ground_truth.items():
    filepath = os.path.join(RECEIPT_FOLDER, filename)

    print("\n========================")
    print(f"Evaluating: {filename}")
    print("========================")

    result = process_receipt_easyocr(filepath)
    extracted = result.get("fields", result)

    for field, expected_value in expected.items():
        total_fields += 1
        extracted_value = extracted.get(field)
        
        # Ensure the field exists in our stats dictionary to avoid KeyErrors
        if field not in field_stats:
            field_stats[field] = {"correct": 0, "total": 0}

        # Step 4: Update total count for this specific field
        field_stats[field]["total"] += 1

        if str(extracted_value) == str(expected_value):
            correct_fields += 1
            # Step 4: Update correct count for this specific field
            field_stats[field]["correct"] += 1

            print(f"[✓] {field}")
            print(f"Expected: {expected_value}")
            print(f"Extracted: {extracted_value}")
        else:
            print(f"[✗] {field}")
            print(f"Expected: {expected_value}")
            print(f"Extracted: {extracted_value}")
        report_rows.append({

    "receipt": filename,

    "field": field,

    "expected": expected_value,

    "extracted": extracted_value,

    "correct": extracted_value == expected_value
})

accuracy = (correct_fields / total_fields) * 100 if total_fields else 0

# Step 5: Print per-field analytics
print("\nFIELD ACCURACY")
print("=" * 30)

for field, stats in field_stats.items():
    # Only calculate and print if the field actually appeared in the tests
    if stats["total"] > 0:
        field_accuracy = (
            stats["correct"] /
            stats["total"] * 100
        )
        print(
            f"{field.capitalize():<10}: "
            f"{stats['correct']}/{stats['total']} "
            f"({field_accuracy:.2f}%)"
        )

# Print overall final results
print("\n========================")
print("FINAL RESULTS")
print("========================")
print(f"Overall Correct : {correct_fields}")
print(f"Overall Total   : {total_fields}")
print(f"Overall Accuracy: {accuracy:.2f}%")
with open(
    "evaluation_report.csv",
    "w",
    newline=""
) as csvfile:

    writer = csv.DictWriter(
        csvfile,
        fieldnames=[
            "receipt",
            "field",
            "expected",
            "extracted",
            "correct"
        ]
    )

    writer.writeheader()

    writer.writerows(report_rows)

print(
    "\nEvaluation report saved to evaluation_report.csv"
)