from abc import ABC

class PreProcessInterface(ABC):
    def preprocess(self, pre_processer_input) -> None:
        """Pre Process pictures for future OCR

        Args:
            pre_processer_input (PreProcesserInput): Pre process input

        """
        raise NotImplementedError("This is just a interface method!")
    
class OCRInterface(ABC):
    def ocr(self, ocr_input):
        """ Generate the OCR from pictures

        Args:
            ocr_input (OCRInput): OCR input
            
        Returns:
            OCRResult: OCR result
        """
        raise NotImplementedError("This is just a interface method!")