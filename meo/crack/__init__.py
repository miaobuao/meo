from .zip import ZipCracker
from .pdf import PdfCracker
from . import utils
class Crack:
    @staticmethod
    def zip(path: str):
        return ZipCracker(path)
    @staticmethod
    def pdf(path: str):
        return PdfCracker(path)
