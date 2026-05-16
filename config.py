import os


class Config:

    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )

    UPLOAD_FOLDER = os.path.join(
        "static",
        "uploads"
    )

    RESULT_FOLDER = "results"

    LOG_FOLDER = "logs"

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg"
    }

    OCR_LANGUAGES = ['en']

    OCR_CONFIDENCE_THRESHOLD = 0.50

    DATABASE_NAME = "receipts.db"