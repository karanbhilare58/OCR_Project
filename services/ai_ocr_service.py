import easyocr
import cv2

from text_cleaner import clean_text
from receipt_parser import parse_receipt


reader = easyocr.Reader(['en'])


def process_receipt_easyocr(filepath):

    img = cv2.imread(filepath)

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

    raw_text = " ".join(detected_text)

    cleaned_text = clean_text(raw_text)

    data = parse_receipt(cleaned_text)

    if confidences:
        avg_conf = sum(confidences) / len(confidences)
    else:
        avg_conf = 0

    data["confidence"] = round(avg_conf * 100, 2)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("static/step_gray.png", gray)

    _, thresh = cv2.threshold(
        gray,
        150,
        255,
        cv2.THRESH_BINARY
    )

    cv2.imwrite("static/step_thresh.png", thresh)

    return data, output_image