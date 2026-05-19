from flask import Flask, request, render_template
from database import db
from models import Receipt
from config import Config
import os

from services.ai_ocr_service import process_receipt_easyocr

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# --- Routes ---

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/receipts')
def view_receipts():
    receipts = Receipt.query.order_by(Receipt.created_at.desc()).all()
    return render_template("receipts.html", receipts=receipts)
@app.route('/receipt/<int:id>')
def receipt_detail(id):

    receipt = Receipt.query.get_or_404(id)

    return render_template(
        "receipt_detail.html",
        receipt=receipt
    )

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'image' not in request.files:
            return render_template("result.html", error="No file uploaded")
            
        file = request.files['image']
        if file.filename == '':
            return render_template("result.html", error="No file selected")

        # Create a temp directory if it doesn't exist
        filepath = "temp_receipt.png"
        file.save(filepath)

        # Process through your Deep Learning OCR pipeline
        result = process_receipt_easyocr(filepath)
        
        # Handle Pipeline Failure safely
        if not result["success"]:
            return render_template("result.html", error=result.get("error", "Unknown OCR error"))

        # Database Logging on Success
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

        # Clean up the temporary file
        if os.path.exists(filepath):
            os.remove(filepath)

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
        return render_template("result.html", error=str(e))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)