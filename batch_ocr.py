import os
import cv2
import pytesseract
import pandas as pd

from text_cleaner import clean_text
from receipt_parser import parse_receipt

input_folder = "data/receipts"

results = []

for filename in os.listdir(input_folder):

    if filename.endswith(".png") or filename.endswith(".jpg"):

        path = os.path.join(input_folder, filename)

        img = cv2.imread(path)

    if img is None:
        print(f"Skipping {filename} (image not found or invalid)")
        continue

    img = cv2.resize(img, None, fx=1.5, fy=1.5)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    raw_text = pytesseract.image_to_string(thresh)

    cleaned_text = clean_text(raw_text)

    data = parse_receipt(cleaned_text)

    data["file"] = filename

    results.append(data)

    print("Processing:", filename)

df = pd.DataFrame(results)

df.to_csv("results.csv", index=False)

print("Processing complete. Results saved to results.csv")