from flask import Flask, request, render_template

from services.ocr_service import process_receipt
from services.ai_ocr_service import process_receipt_easyocr

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['image']

    filepath = "temp_receipt.png"

    file.save(filepath)

    data, output_image = process_receipt_easyocr(filepath)

    return render_template(
        "result.html",
        data=data,
        image=output_image,
        original="static/original.png",
        gray="static/step_gray.png",
        thresh="static/step_thresh.png"
    )


if __name__ == "__main__":
    app.run(debug=True)