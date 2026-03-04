import cv2
import pytesseract
import pandas as pd
import config
from receipt_parser import parse_receipt
from text_cleaner import clean_text

img = cv2.imread("test.png")
img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

raw_text = pytesseract.image_to_string(thresh)
text = clean_text(raw_text)

print("RAW TEXT:\n", raw_text)

print("\nCLEANED TEXT:\n", text)

data = parse_receipt(text)

print("\nSTRUCTURED DATA:")
print(data)

# Save results to CSV
df = pd.DataFrame([data])
df.to_csv("receipt_results.csv", mode="a", header=False, index=False)