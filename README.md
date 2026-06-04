# AI Receipt OCR System

An end-to-end AI-powered Receipt OCR System that extracts structured financial information from receipt images using Computer Vision, OCR, NLP, and a Flask web application.

## Overview

The system automatically processes receipt images and extracts key financial fields such as:

* Date
* Subtotal
* Tax
* Total Amount

The application combines image preprocessing, OCR, text normalization, intelligent receipt parsing, database storage, REST APIs, and evaluation analytics into a production-style pipeline.

## Features

* EasyOCR-powered text extraction
* OpenCV image preprocessing
* Intelligent receipt parsing
* Date, subtotal, tax, and total extraction
* Receipt history management
* SQLite database integration
* Batch receipt processing
* REST API support
* Swagger API documentation
* Evaluation framework
* CSV evaluation reporting
* Docker containerization

## Tech Stack

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* SQLite

### AI / OCR

* EasyOCR
* OpenCV
* spaCy

### Documentation

* Flasgger (Swagger UI)

### Deployment

* Docker

## System Architecture

Receipt Image
↓
OpenCV Preprocessing
↓
EasyOCR
↓
Text Cleaning & Normalization
↓
Receipt Parser
↓
Field Extraction
↓
Database Storage
↓
Web Interface / REST API

## Project Structure

OCR_Project/

├── app.py

├── database.py

├── models.py

├── receipt_parser.py

├── text_cleaner.py

├── evaluate.py

├── batch_ocr.py

├── services/

│ ├── ai_ocr_service.py

│ ├── nlp_service.py

│ └── receipt_service.py

├── templates/

├── static/

├── data/

├── tests/

├── Dockerfile

└── requirements-docker.txt

## API Endpoints

### Process Single Receipt

POST

/api/process_receipt

Accepts a receipt image and returns extracted fields.

### Batch Receipt Processing

POST

/api/process_batch

Accepts multiple receipt images and processes them together.

### Swagger Documentation

/apidocs

Interactive API documentation generated using Flasgger.

## Evaluation Results

Benchmark Dataset:

* 17 receipt images
* Multiple receipt formats
* Realistic OCR noise

### Field Accuracy

| Field    | Accuracy |
| -------- | -------- |
| Date     | 100.00%  |
| Subtotal | 93.33%   |
| Tax      | 100.00%  |
| Total    | 94.12%   |

### Overall Accuracy

96.83%

61 Correct Fields / 63 Total Fields

### Evaluation Reporting

The project automatically generates:

evaluation_report.csv

containing:

* Receipt Name
* Field Name
* Expected Value
* Extracted Value
* Pass/Fail Status

## Screenshots

### Home Page

(Add Screenshot)

### OCR Result Page

(Add Screenshot)

### Receipt History

(Add Screenshot)

### Swagger Documentation

(Add Screenshot)

### Docker Execution

(Add Screenshot)

## Installation

### Clone Repository

git clone YOUR_GITHUB_LINK

cd OCR_Project

### Create Virtual Environment

python -m venv venv

source venv/bin/activate

### Install Dependencies

pip install -r requirements-docker.txt

### Run Application

python app.py

Application:

http://localhost:5000

Swagger:

http://localhost:5000/apidocs

## Docker

### Build Image

docker build -t receipt-ocr .

### Run Container

docker run -p 5000:5000 receipt-ocr

## Challenges Solved

* OCR text cleaning and normalization
* Receipt format variability
* Total amount extraction accuracy
* Batch receipt processing
* Evaluation and benchmarking
* Docker containerization

## Future Improvements

* Cloud deployment
* Multi-language receipt support
* Receipt classification
* Expense analytics dashboard
* Deep learning-based field extraction
* PDF receipt processing

## Resume Highlights

* Built an end-to-end OCR system using EasyOCR, OpenCV, Flask, and SQLite.
* Developed REST APIs, batch processing, database persistence, and evaluation analytics.
* Achieved 96.83% field extraction accuracy on a custom benchmark dataset.
* Containerized the application using Docker for reproducible deployment.

## Author

Karan Bhilare

GitHub: YOUR_GITHUB_LINK
