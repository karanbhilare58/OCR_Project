FROM python:3.11-slim

WORKDIR /app

COPY requirements-docker.txt .

RUN pip install --no-cache-dir -r requirements-docker.txt

RUN python -m spacy download en_core_web_sm

COPY . .

RUN mkdir -p logs static instance

EXPOSE 5000

CMD ["python", "app.py"]


