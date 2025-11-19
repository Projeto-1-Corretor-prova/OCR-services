FROM python:3.11-alpine as base

WORKDIR /service

RUN apk add --no-cache build-base cmake clang python3-dev py3-numpy-dev \
    libjpeg-turbo-dev libpng-dev tiff-dev libwebp-dev openjpeg-dev \
    openblas-dev libtbb-dev

RUN apk add --update tesseract-ocr tesseract-ocr-data-eng tesseract-ocr-data-por

COPY requirements.txt /service/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt --verbose

COPY . /service/

EXPOSE $PORT

ENTRYPOINT [ "uvicorn", "app.app:app", "--port", "$PORT", "--host", "$0.0.0.0" ]