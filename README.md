# OCR Receipt Processing System

## Overview
This project extracts structured data from receipt images using Tesseract OCR and OpenCV preprocessing.

## Features
- Image preprocessing
- OCR text extraction
- Structured receipt parsing
- Data output formatting

## Technologies Used
- Python
- OpenCV
- Tesseract OCR
- Regex (Data Parsing)

## How to Run

1. Install dependencies:
pip install -r requirements.txt

2. Install Tesseract OCR

3. Run:
python test_ocr.py

## Example Output

{
  "order_number": "873598590",
  "date": "07/09/20",
  "subtotal": 3899.00,
  "tax": 341.16,
  "total": 4240.16
}
