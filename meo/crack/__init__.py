from .zip import ZipCracker
from .pdf import PDFCracker
from . import utils
class Crack:
    @staticmethod
    def zip(path: str):
        return ZipCracker(path)
    @staticmethod
    def pdf(path: str):
        return PDFCracker(path)
