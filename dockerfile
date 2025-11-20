FROM python:3.11-slim as base

WORKDIR /service

RUN apt update

RUN apt install -y libtesseract-dev tesseract-ocr tesseract-ocr-eng tesseract-ocr-por libgl1

COPY requirements.txt /service/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt --verbose

COPY app /service/app

COPY src /service/src

ENTRYPOINT ["uvicorn", "app.app:app", "--host" , "0.0.0.0", "--port", "8000"]
