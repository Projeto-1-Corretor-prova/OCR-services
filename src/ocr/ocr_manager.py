from pytesseract import image_to_string
from PIL.Image import open as open_image

from os import listdir

from re import split

from src.interfaces import OCRInterface
from src.settings import Settings
from src.ocr.models import Answer, Correction, OCRInput, OCRResult

#return {"ocr": image_to_string(image_bytes, lang=Settings.tesseract_language, config=Settings.tesseract_configuration)}

class OCRManager(OCRInterface):
    def __init__(self):
        super().__init__()

    def ocr(self, ocr_input: OCRInput) -> OCRResult:
        result: OCRResult = dict()
        
        result["corrections"] = list()
        
        students_path = ocr_input["ocr_path"]
        
        students = [student for student in listdir(students_path)]
        
        for student in students:
            student_path = f"{ocr_input['ocr_path']}/{student}"
            
            correction_turn: Correction = dict()
            result["corrections"].append(correction_turn)
            
            correction_turn["student_id"] = student
            correction_turn["answers"] = list()
            
            last_answer: Answer = None
            
            for page in sorted(listdir(student_path)):
                page_path = f"{student_path}/{page}"
                page_image_bytes = open_image(page_path)
                
                page_text = image_to_string(
                    page_image_bytes, 
                    lang=Settings.tesseract_language, 
                    config=Settings.tesseract_configuration
                    )
                
                answers = split(ocr_input["regex_question"], page_text)
                
                # print(f"Na página: {page}, lemos {len(answers)} respostas")
                
                for answer in answers[1:]:
                    answer_correction: Answer = {"answer": answer, "question_id": len(correction_turn["answers"])}
                    correction_turn["answers"].append(answer_correction)
                
                if last_answer:
                    last_answer["answer"] += answers[0]
                
                if correction_turn["answers"]:
                    last_answer = correction_turn["answers"][-1]
                
                
        return result