from pyzipper import ZipFile
from .cracker import Cracker

class ZipCracker(Cracker):
    
    def try_open(self, zfile: ZipFile, pwd: bytes, mem: str):
        assert isinstance(zfile, ZipFile) and isinstance(pwd, bytes)
        try:
            with zfile.open(mem, pwd=pwd) as f:
                if f.seek(1):
                    return True
        except ValueError as e:
            raise e
        except:
            return False

    def step_once(self, pwd: bytes) -> bytes | None:
        zfile = ZipFile(self.path)
        mem = zfile.filelist[0].filename
        if self.try_open(zfile, pwd, mem):
            return pwd
        return None
    
    def step_some(self, *pwds: bytes) -> bytes | None:
        zfile = ZipFile(self.path)
        mem = zfile.filelist[0].filename
        for pwd in pwds:
            if self.try_open(zfile, pwd, mem):
                return pwd
        del pwds
        return None
