import os

from models import Receipt
from database import db

from services.ai_ocr_service import process_receipt_easyocr


ALLOWED_EXTENSIONS = {
    'png',
    'jpg',
    'jpeg'
}


def allowed_file(filename):

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_receipt_file(file, upload_folder):

    if file.filename == '':

        return {
            "success": False,
            "error": "Empty filename"
        }, 400

    if not allowed_file(file.filename):

        return {
            "success": False,
            "error": "Invalid file type"
        }, 400

    filepath = os.path.join(
        upload_folder,
        file.filename
    )

    file.save(filepath)

    result = process_receipt_easyocr(filepath)

    if os.path.exists(filepath):
        os.remove(filepath)

    return result, 200


def save_receipt_to_db(filename, result):

    receipt = Receipt(

        filename=filename,

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

    return receipt