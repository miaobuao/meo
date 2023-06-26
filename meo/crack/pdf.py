from pikepdf import Pdf, PasswordError
from .cracker import Cracker
from ..io import encode

class PdfCracker(Cracker):
    def remove_pdf_password(self, output_path: str, pwd=b''):
        with Pdf.open(self.path, password=pwd) as f:
            f.save(output_path)
            
    def test(self, pwd=b''):
        try:
            with Pdf.open(self.path, password=pwd) as f:
                return True
        except PasswordError:
            return False

    def step_once(self, pwd: bytes) -> bytes | None:
        if self.test(pwd):
            return pwd
        return None
    
    def step_some(self, *pwds: bytes) -> bytes | None:
        for pwd in pwds:
            if self.test(pwd):
                return pwd
        return None
