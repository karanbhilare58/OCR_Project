from urllib import response

import easyocr
import cv2
import uuid

from text_cleaner import clean_text, normalize_ocr_text
from receipt_parser import parse_receipt

import logging
import time

import os

os.makedirs(
    "logs",
    exist_ok=True
)

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

reader = easyocr.Reader(['en'])


def process_receipt_easyocr(filepath):

    try:

        start_time = time.time()

        unique_id = str(uuid.uuid4())

        img = cv2.imread(filepath)

        if img is None:
            raise ValueError("Invalid image uploaded")

        # =========================
        # IMAGE PREPROCESSING
        # =========================

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        thresh = cv2.threshold(
            gray,
            150,
            255,
            cv2.THRESH_BINARY
        )[1]

        # =========================
        # UNIQUE IMAGE PATHS
        # =========================

        original_path = f"static/{unique_id}_original.png"
        gray_path = f"static/{unique_id}_gray.png"
        thresh_path = f"static/{unique_id}_thresh.png"
        processed_path = f"static/{unique_id}_processed.png"

        # =========================
        # SAVE PIPELINE IMAGES
        # =========================

        cv2.imwrite(original_path, img)
        cv2.imwrite(gray_path, gray)
        cv2.imwrite(thresh_path, thresh)

        # =========================
        # OCR
        # =========================

        results = reader.readtext(filepath)

        detected_text = []

        confidences = []

        # Draw bounding boxes
        boxed_img = img.copy()

        for result in results:

            box = result[0]
            text = result[1]
            confidence = result[2]

            detected_text.append(text)

            confidences.append(confidence)

            # Bounding box coordinates
            top_left = tuple(map(int, box[0]))
            bottom_right = tuple(map(int, box[2]))

            cv2.rectangle(
                boxed_img,
                top_left,
                bottom_right,
                (0, 255, 0),
                2
            )

        cv2.imwrite(processed_path, boxed_img)

        # =========================
        # TEXT PROCESSING
        # =========================
        raw_text = " ".join(detected_text)
        cleaned_text = clean_text(raw_text)

        cleaned_text = normalize_ocr_text(cleaned_text)

        data = parse_receipt(cleaned_text)

        processing_time = round(
            time.time() - start_time,
            2
        )

        confidence_score = 0

        if confidences:

            confidence_score = round(
                sum(confidences) / len(confidences) * 100,
                2
            )

        logging.info(
            f"OCR processed successfully in {processing_time} seconds"
        )

        # =========================
        # FINAL RESPONSE
        # =========================

        response = {

            "success": True,

            "ocr": {

                "raw_text": raw_text,

                "confidence": confidence_score
            },

            "fields": data,

            "metadata": {

                "processing_time": processing_time,

                "ocr_engine": "EasyOCR"
            },

            "images": {

                "original": original_path,

                "gray": gray_path,

                "threshold": thresh_path,

                "processed": processed_path
            }
        }

        return response

    except Exception as e:

        logging.error(
            f"OCR Processing Failed: {str(e)}"
        )

        return {

            "success": False,

            "error": str(e)
        }