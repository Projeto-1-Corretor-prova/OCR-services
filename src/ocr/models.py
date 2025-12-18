from typing_extensions import TypedDict

class OCRInput(TypedDict):
    ocr_path: str
    regex_question: str

class Answer(TypedDict):
    question_id: int
    answer: str

class Correction(TypedDict):
    student_id: str
    answers: list[Answer]

class OCRResult(TypedDict):
    corrections: list[Correction]