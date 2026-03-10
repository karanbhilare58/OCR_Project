# 🧾 AI Receipt OCR System

An end-to-end **Optical Character Recognition (OCR) pipeline** that extracts structured data from receipt images using **OpenCV, Tesseract OCR, and Flask**.

The system preprocesses receipt images, detects text regions, extracts important information (Date, Subtotal, Tax, Total), calculates OCR confidence, and visualizes the entire processing pipeline through a web interface.

---

## 🚀 Demo

Upload a receipt image and the system will:

1. Preprocess the image  
2. Extract text using OCR  
3. Detect text regions  
4. Extract structured data  
5. Display confidence and results  

---

## 🖥️ Application Interface

### Upload Receipt
Upload a receipt image through the web interface.

### OCR Processing Pipeline
The system visually shows each step of the OCR pipeline:

• Original Image  
• Grayscale Conversion  
• Threshold Processing  
• OCR Detection (Bounding Boxes)

### Extracted Data
The system automatically extracts:

• Date  
• Subtotal  
• Tax  
• Total  
• OCR Confidence Score  

---

## 🧠 System Architecture

Receipt Image  
↓  
OpenCV Image Preprocessing  
↓  
Grayscale Conversion  
↓  
Thresholding  
↓  
Tesseract OCR  
↓  
Text Cleaning  
↓  
Regex Information Extraction  
↓  
Confidence Calculation  
↓  
Flask Web Visualization  

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| OpenCV | Image preprocessing |
| Tesseract OCR | Text recognition |
| Flask | Web application backend |
| Bootstrap | User interface |
| Pandas | Data handling |
| Regex | Structured data extraction |

---

## 📂 Project Structure

OCR_PROJECT2  
│  
├── app.py                # Flask web application  
├── batch_ocr.py          # Batch OCR processing script  
├── text_cleaner.py       # OCR text cleaning module  
├── receipt_parser.py     # Regex data extraction  
│  
├── templates  
│   ├── index.html        # Upload page  
│   └── result.html       # Result display page  
│  
├── static  
│   ├── original.png  
│   ├── step_gray.png  
│   ├── step_thresh.png  
│   └── processed_receipt.png  
│  
├── data  
│   └── receipts          # Sample receipt images  
│  
└── results               # OCR output results  

---

## ⚙️ Installation

Clone the repository

    git clone https://github.com/karanbhilare58/OCR_Project2.git

Navigate to the project folder

    cd OCR_Project2

Create virtual environment

    python -m venv venv

Activate environment

    venv\Scripts\activate

Install dependencies

    pip install -r requirements.txt

---

## ▶️ Run the Application

Start the Flask server

    python app.py

Open browser

    http://127.0.0.1:5000

Upload a receipt image and view extracted results.

---

## 📊 Example Output

Date: 07/09/20  
Subtotal: 3899.00  
Tax: 341.16  
Total: 4240.16  
OCR Confidence: 76.53%

The system also displays the OCR processing pipeline showing image preprocessing steps and detected text regions.

---

## ✨ Features

✔ Interactive web interface  
✔ End-to-end OCR pipeline  
✔ Visual preprocessing stages  
✔ Bounding box text detection  
✔ Structured data extraction  
✔ OCR confidence scoring  

---
