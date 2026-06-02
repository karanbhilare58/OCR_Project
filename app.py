from database import db
from models import Receipt
from config import Config

import os

from flask import Flask, render_template, request, jsonify
from flasgger import Swagger

from services.ai_ocr_service import process_receipt_easyocr
from services.receipt_service import (
    process_receipt_file,
    save_receipt_to_db
)


app = Flask(__name__)

app.config.from_object(Config)

swagger = Swagger(app)

db.init_app(app)


# =========================
# Create Upload Folder
# =========================

os.makedirs(
    app.config['UPLOAD_FOLDER'],
    exist_ok=True
)


# =========================
# Allowed File Extensions
# =========================

ALLOWED_EXTENSIONS = {
    'png',
    'jpg',
    'jpeg'
}


def allowed_file(filename):

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# =========================
# Home Route
# =========================

@app.route('/')
def home():

    return render_template("index.html")


# =========================
# Receipt History Route
# =========================

@app.route('/receipts')
def view_receipts():

    receipts = Receipt.query.order_by(
        Receipt.created_at.desc()
    ).all()

    return render_template(
        "receipts.html",
        receipts=receipts
    )


# =========================
# Receipt Detail Route
# =========================

@app.route('/receipt/<int:id>')
def receipt_detail(id):

    receipt = Receipt.query.get_or_404(id)

    return render_template(
        "receipt_detail.html",
        receipt=receipt
    )


# =========================
# Web Upload Route
# =========================

@app.route('/upload', methods=['POST'])
def upload():

    try:

        if 'image' not in request.files:

            return render_template(
                "result.html",
                error="No file uploaded"
            )

        file = request.files['image']

        result, status_code = process_receipt_file(
    file,
    app.config['UPLOAD_FOLDER']
)

        if not result["success"]:

            return render_template(
                "result.html",
                error=result["error"]
            )

        save_receipt_to_db(
    file.filename,
    result
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


# =========================
# API OCR Route
# =========================

@app.route('/api/process_receipt', methods=['POST'])
def api_process_receipt():

    """
    Process Receipt API
    ---
    tags:
      - OCR API

    consumes:
      - multipart/form-data

    parameters:
      - name: receipt
        in: formData
        type: file
        required: true
        description: Upload receipt image

    responses:
      200:
        description: OCR processed successfully

      400:
        description: Invalid request or file

      500:
        description: Internal server error
    """

    try:

        if 'receipt' not in request.files:

            return jsonify({

                "success": False,
                "error": "No receipt image uploaded"

            }), 400

        file = request.files['receipt']

        result, status_code = process_receipt_file(
    file,
    app.config['UPLOAD_FOLDER']
)

        return jsonify(result), status_code

    except Exception as e:

        return jsonify({

            "success": False,
            "error": str(e)

        }), 500
    
@app.route('/api/process_batch', methods=['POST'])
def api_process_batch():

    if 'receipts' not in request.files:

        return jsonify({

            "success": False,
            "error": "No receipt images uploaded"

        }), 400

    files = request.files.getlist('receipts')

    if len(files) == 0:

        return jsonify({

            "success": False,
            "error": "Empty upload"

        }), 400

    results = []

    for file in files:

        if file.filename == '':

            continue

        if not allowed_file(file.filename):

            results.append({

                "filename": file.filename,
                "success": False,
                "error": "Invalid file type"

            })

            continue

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            file.filename
        )

        file.save(filepath)

        result = process_receipt_easyocr(filepath)
        if os.path.exists(filepath):
            os.remove(filepath)

        results.append({

            "filename": file.filename,
            "result": result

        })

    return jsonify({

        "success": True,
        "total_processed": len(results),
        "results": results

    })

# =========================
# Main Entry
# =========================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(
    host="0.0.0.0",
    port=5000,
    debug=False
    )