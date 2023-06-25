from pikepdf import Pdf
from .cracker import Cracker

class PDFCracker(Cracker):
    def try_open(self, zfile: Pdf, pwd: bytes, mem: str):
        assert isinstance(zfile, Pdf) and isinstance(pwd, bytes)
        try:
            with zfile.open(mem, pwd=pwd) as f:
                if f.seek(1):
                    return True
        except ValueError as e:
            raise e
        except:
            return False

    def step_once(self, pwd: bytes) -> bytes | None:
        zfile = Pdf(self.path)
        mem = zfile.filelist[0].filename
        if self.try_open(zfile, pwd, mem):
            return pwd
        return None
    
    def step_some(self, *pwds: bytes) -> bytes | None:
        zfile = Pdf(self.path)

if __name__ == '__main__':
    pdf = PDFCracker("./examples/data/cannot_open.pdf")
    pdf.drop_psw_and_save("./test/unlock.pdf")