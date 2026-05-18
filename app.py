from flask import Flask, request, render_template
from database import db
from models import Receipt
from config import Config

from services.ai_ocr_service import process_receipt_easyocr


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


@app.route('/')
def home():

    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():

    try:

        file = request.files['image']

        filepath = "temp_receipt.png"

        file.save(filepath)

        result = process_receipt_easyocr(filepath)
        if result["success"]:

            receipt = Receipt(

            filename=file.filename,

            date=result["fields"]["date"],

            subtotal=result["fields"]["subtotal"],

            tax=result["fields"]["tax"],

            total=result["fields"]["total"],

            confidence=result["ocr"]["confidence"],

            processing_time=result["metadata"]["processing_time"],

            raw_text=result["ocr"]["raw_text"],

            ocr_engine=result["metadata"]["ocr_engine"]
        )

        db.session.add(receipt)

        db.session.commit()
        
        if not result["success"]:

            return render_template(
                "result.html",
                error=result["error"]
            )

        return render_template(

            "result.html",

            data=result["fields"],

            confidence=result["ocr"]["confidence"],

            processing_time=result["metadata"]["processing_time"],

            image=result["images"]["processed"],

            original=result["images"]["original"],

            gray=result["images"]["gray"],

            thresh=result["images"]["threshold"]
        )

    except Exception as e:

        return render_template(
            "result.html",
            error=str(e)
        )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)