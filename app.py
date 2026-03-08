from flask import Flask, request, render_template
import cv2
import pytesseract
from pytesseract import Output

from text_cleaner import clean_text
from receipt_parser import parse_receipt

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['image']

    filepath = "temp_receipt.png"
    file.save(filepath)

    img = cv2.imread(filepath)

    img = cv2.resize(img, None, fx=1.5, fy=1.5)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)

    ocr_data = pytesseract.image_to_data(thresh, output_type=Output.DICT)

    confidences = ocr_data["conf"]

    valid_conf = []

    for conf in confidences:
        try:
            conf = float(conf)
            if conf > 0:
                valid_conf.append(conf)
        except:
            pass

    if valid_conf:
        avg_conf = sum(valid_conf) / len(valid_conf)
    else:
        avg_conf = 0

    n_boxes = len(ocr_data['text'])

    for i in range(n_boxes):

        try:
            conf = float(ocr_data['conf'][i])
        except:
            conf = -1

        if conf > 60:

            x = ocr_data['left'][i]
            y = ocr_data['top'][i]
            w = ocr_data['width'][i]
            h = ocr_data['height'][i]

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0),2)

    words = ocr_data["text"]

    raw_text = " ".join(words)

    cleaned_text = clean_text(raw_text)

    data = parse_receipt(cleaned_text)
    
    data["confidence"] = round(avg_conf, 2)

    output_image = "static/output.png"

    cv2.imwrite(output_image, img)

    return render_template("result.html", data=data, image=output_image)


if __name__ == "__main__":
    app.run(debug=True)