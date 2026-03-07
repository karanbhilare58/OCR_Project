import os
import cv2
import pytesseract
from pytesseract import Output
import pandas as pd

from text_cleaner import clean_text
from receipt_parser import parse_receipt

input_folder = "data/receipts"

# ensure results folder exists
os.makedirs("results", exist_ok=True)

results = []

for filename in os.listdir(input_folder):

    if filename.endswith(".png") or filename.endswith(".jpg"):

        path = os.path.join(input_folder, filename)

        img = cv2.imread(path)

        if img is None:
            print(f"Skipping {filename} (image not found or invalid)")
            continue

        print("Processing:", filename)

        img = cv2.resize(img, None, fx=1.5, fy=1.5)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # OCR with detailed data
        ocr_data = pytesseract.image_to_data(thresh, output_type=Output.DICT)

        n_boxes = len(ocr_data['text'])

        words = []
        valid_conf = []

        for i in range(n_boxes):

            word = ocr_data['text'][i]
            conf = float(ocr_data['conf'][i])

            if word.strip() != "":
                words.append(word)

            if conf > 0:
                valid_conf.append(conf)

            # draw bounding boxes for confident detections
            if conf > 60:

                x = ocr_data['left'][i]
                y = ocr_data['top'][i]
                w = ocr_data['width'][i]
                h = ocr_data['height'][i]

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                cv2.putText(
                    img,
                    word,
                    (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1
                )

        # save image with boxes
        output_path = os.path.join("results", filename)
        cv2.imwrite(output_path, img)

        # calculate confidence
        avg_conf = sum(valid_conf) / len(valid_conf) if valid_conf else 0

        raw_text = " ".join(words)

        cleaned_text = clean_text(raw_text)

        data = parse_receipt(cleaned_text)

        data["raw_text"] = cleaned_text[:200]
        data["confidence"] = round(avg_conf, 2)
        data["file"] = filename

        results.append(data)

df = pd.DataFrame(results)

df.to_csv("results.csv", index=False)

print("Processing complete. Results saved to results.csv")