import easyocr
import cv2

from text_cleaner import clean_text
from receipt_parser import parse_receipt

import logging
import time

from config import Config


logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


reader = easyocr.Reader(Config.OCR_LANGUAGES)


def process_receipt_easyocr(filepath):

    try:

        start_time = time.time()

        img = cv2.imread(filepath)

        if img is None:
            raise ValueError("Invalid image uploaded")

        cv2.imwrite("static/original.png", img)

        results = reader.readtext(filepath)

        detected_text = []

        confidences = []

        for result in results:

            box = result[0]
            text = result[1]
            confidence = result[2]

            detected_text.append(text)

            confidences.append(confidence)

            top_left = tuple(map(int, box[0]))
            bottom_right = tuple(map(int, box[2]))

            cv2.rectangle(
                img,
                top_left,
                bottom_right,
                (0, 255, 0),
                2
            )

            cv2.putText(
                img,
                text,
                (top_left[0], top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )

        output_image = "static/processed_receipt.png"

        cv2.imwrite(output_image, img)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cv2.imwrite("static/step_gray.png", gray)

        _, thresh = cv2.threshold(
            gray,
            150,
            255,
            cv2.THRESH_BINARY
        )

        cv2.imwrite("static/step_thresh.png", thresh)

        raw_text = " ".join(detected_text)

        cleaned_text = clean_text(raw_text)

        data = parse_receipt(cleaned_text)

        if confidences:
            avg_conf = round(
                sum(confidences) / len(confidences) * 100,
                2
            )
        else:
            avg_conf = 0

        processing_time = round(
            time.time() - start_time,
            2
        )

        response = {

            "success": True,

            "ocr": {
                "raw_text": raw_text,
                "confidence": avg_conf
            },

            "fields": {
                "date": data.get("date"),
                "subtotal": data.get("subtotal"),
                "tax": data.get("tax"),
                "total": data.get("total")
            },

            "metadata": {
                "processing_time": processing_time,
                "ocr_engine": "EasyOCR"
            },

            "images": {
                "processed": output_image,
                "original": "static/original.png",
                "gray": "static/step_gray.png",
                "threshold": "static/step_thresh.png"
            }
        }

        logging.info(
            f"OCR processed successfully in {processing_time} seconds"
        )

        return response

    except Exception as e:

        logging.error(
            f"OCR Processing Failed: {str(e)}"
        )

        return {
            "success": False,
            "error": str(e)
        }