from database import db


class Receipt(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    filename = db.Column(
        db.String(200)
    )

    date = db.Column(
        db.String(100)
    )

    subtotal = db.Column(
        db.String(100)
    )

    tax = db.Column(
        db.String(100)
    )

    total = db.Column(
        db.String(100)
    )

    confidence = db.Column(
        db.Float
    )

    processing_time = db.Column(
        db.Float
    )

    raw_text = db.Column(
        db.Text
    )

    ocr_engine = db.Column(
        db.String(100)
    )