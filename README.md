# OCR Service Repository

Here you can work on try integrate the ocr feature in our platform. All logic and business code will be in a single place to help your work!

## Table of Contents
1. [Work Environment](#create-your-work-environment)
2. [Repository Tree Structure](#repository-tree-structure)
3. [Service Usage](#service-usage)

## Create your Work Environment

Before all instructions, you need the tesseract-ocr package installed on your local machine. Please see this [link](https://tesseract-ocr.github.io/tessdoc/Installation.html).

Please, you will need python to work on this repository, a python environment manager is recommended ([venv](https://docs.python.org/pt-br/3/library/venv.html) or [anaconda/miniconda](https://www.anaconda.com/download/success)).

Python version (used by the repository author): 3.11.

After that, you just need (on repository root dir):

```
bash
pip install -r requirements
```

## Repository Tree Structure 

```
.
├── app // app dir (all logic on services communication)
│   ├── app.py // main file for this service application
│   ├── ... // logic logic on services communication files/dirs
├── docker-compose.yaml // Run the Container on github organization or build a new package from your machine!
├── dockerfile // Build docker file configuration
├── data // data dir (input and output root dir to any experiment)
│   ├── .keep
├── .env.example // .env.example to configure service
├── README.md // This file
├── requirements.txt // pip requirements.
└── src // source code and logic code
    ├── interfaces.py // Interface to repository usage
    ├── ocr // OCR logic
    │   ├── __init__.py
    │   ├── ...
    ├── preprocess // Pre process logic
    │   ├── __init__.py
    │   ├── ...
    └── settings.py // Environment variables 
```

## Service Usage

First of all, update your environment variables on .env file (If you don't have one, create from .env.example).

If you want use locally in your python environment, you can just use this bash commands:

```
bash
pip install -r requirements
source .env
uvicorn app.app:app --port $PORT --host 0.0.0.0
```

If you want use from docker compose, you can just use this bash commands (Remember, you will need docker and docker compose v2 to use it):

```
bash
docker compose up --build
```