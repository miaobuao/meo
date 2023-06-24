import zipfile
import asyncio
from tqdm.asyncio import tqdm
from itertools import permutations
import multiprocessing
import itertools

PWD_SEED = b"1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM!@#$%^&*()_+-=[{}]\|;:,<.>/?'\" "

def try_open_zip(zfile: zipfile.ZipFile, pwd: bytes):
    assert isinstance(zfile, zipfile.ZipFile) and isinstance(pwd, bytes)
    try:
        mem = zfile.filelist[0].filename
        with zfile.open(mem, pwd=pwd) as f:
            if f.seek(1):
                return True
    except ValueError as e:
        raise e
    except:
        return False
    
def guess_number_pwd(path, start=0, end=1e99, step=1):
    zfile = zipfile.ZipFile(path)
    for number in tqdm(range(start, end, step)):
        pwd = str(number).encode("utf8")
        if try_open_zip(zfile, pwd):
            return pwd
    return None
            
def key_permution(seed, size):
    for k in permutations(seed, size):
        yield bytes(k)

def key_generator(start=None, end=None, seed=PWD_SEED):
    n_size = 0 if start is None else int(start)
    if end is None:
        while True:
            n_size += 1
            for k in key_permution(seed, n_size):
                yield k, n_size
    else:
        end = int(end)
        while True:
            n_size += 1
            if n_size <= end:
                for k in key_permution(seed, n_size):
                    yield k, n_size

async def guess_async(path, min_length=None, max_length=None, seed=PWD_SEED):
    zfile = zipfile.ZipFile(path)

    async def block(pwd):
        if try_open_zip(zfile, pwd):
            return pwd
        return False
    
    with tqdm(key_generator(min_length, max_length, seed=seed)) as bar:
        async for pwd, _ in bar:
            if await block(pwd):
                return pwd
    return None

def guess_pwd_normal(path, min_length=None, max_length=None, seed=PWD_SEED):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(guess_async(path, min_length, max_length, seed))
    loop.run_until_complete(future)
    pwd = future.result()
    return pwd

def __guess_step(path, pwds: list[tuple[bytes, int]]):
    zfile = zipfile.ZipFile(path)
    for pwd, _ in pwds:
        if try_open_zip(zfile, pwd):
            return pwd
    return False

def guess_in_multiprocess(path, min_length=None, max_length=None, n_processes=8, slice_size=500, seed=PWD_SEED):
    pool = multiprocessing.Pool(n_processes)
    it = key_generator(min_length, max_length, seed=seed)
    manager = multiprocessing.Manager()
    info = manager.dict()
    info['key'] = None
    def cb(re):
        if re:
            info['key'] = re
            pool.terminate()
    while True:
        for _ in range(n_processes):
            try:
                pwds = itertools.islice(it, 0, slice_size)
                pool.apply_async(__guess_step, (path, list(pwds)), callback=cb, error_callback=print)
            except StopIteration:
                pool.terminate()
                return None
            except Exception as e:
                if e.args[0] == 'Pool not running':
                    return info['key']
                else:
                    raise e

class ZipPasswordGuesser:

    def __init__(self, path, seed=PWD_SEED) -> None:
        assert isinstance(seed, bytes)
        self.seed = seed
        self.path = path

    def only_number(self):
        return guess_number_pwd(self.path)
    
    async def by_seed_async(self, min_length=None, max_length=None):
        return await guess_async(self.path, min_length, max_length, seed=self.seed)
    
    def by_seed(self, min_length=None, max_length=None):
        return guess_pwd_normal(self.path, min_length, max_length, seed=self.seed)
    
    def by_seed_mp(self, min_length=None, max_length=None, n_processes=8, slice_size=500):
        return guess_in_multiprocess(self.path, min_length, max_length, n_processes, slice_size, seed=self.seed)


class Crack:
    @staticmethod
    def zip(path: str, seed=PWD_SEED):
        return ZipPasswordGuesser(path, seed)
    

if __name__ == '__main__':
    zg = Crack.zip("./examples/flag.zip")
    k = zg.by_seed_mp()
    print(k)