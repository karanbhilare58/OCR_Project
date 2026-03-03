import cv2
import pytesseract
import config
from receipt_parser import parse_receipt

img = cv2.imread("test.png")
img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

text = pytesseract.image_to_string(thresh)

print("RAW TEXT:\n", text)

data = parse_receipt(text)

print("\nSTRUCTURED DATA:")
print(data)