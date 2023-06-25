from pyzipper import ZipFile
import asyncio
from tqdm.asyncio import tqdm
from itertools import permutations
import multiprocessing
import itertools
import gc
from functools import partial
from tqdm.asyncio import tqdm

PWD_SEED_NUMBER = b"0123456789"
PWD_SEED_LOWER_ALPHABET = b'qwertyuiopasdfghjklzxcvbnm'
PWD_SEED_UPPER_ALPHABET = b'QWERTYUIOPASDFGHJKLZXCVBNM'
PWD_SEED_SPECIAL_CHAR = b'!@#$%^&*()_+-=[{}]\|;:,<.>/?\'" '
PWD_SEED_ALPHABET = PWD_SEED_LOWER_ALPHABET + PWD_SEED_UPPER_ALPHABET
PWD_SEED_SIMPLE = PWD_SEED_LOWER_ALPHABET + PWD_SEED_NUMBER
PWD_SEED_COMPLEX = PWD_SEED_ALPHABET + PWD_SEED_SPECIAL_CHAR + PWD_SEED_NUMBER

def try_open_zip(zfile: ZipFile, pwd: bytes):
    assert isinstance(zfile, ZipFile) and isinstance(pwd, bytes)
    try:
        mem = zfile.filelist[0].filename
        with zfile.open(mem, pwd=pwd) as f:
            if f.seek(1):
                return True
    except ValueError as e:
        raise e
    except:
        return False
    
def guess_number_pwd(path, start=0, end=None, step=1, progressbar=False):
    zfile = ZipFile(path)
    start = int(start)
    if end is None:
        now = start
        while True:
            pwd = str(now).encode("utf8")
            if try_open_zip(zfile, pwd):
                return pwd
            now += step
    end = int(end)
    bar = range(start, end, step)
    if progressbar:
        bar = tqdm(bar)
    for number in bar:
        pwd = str(number).encode("utf8")
        if try_open_zip(zfile, pwd):
            return pwd
    return None
            
def key_permution(seed, size):
    for k in permutations(seed, size):
        yield bytes(k)

def key_generator(start=None, end=None, seed=PWD_SEED_COMPLEX):
    n_size = 1 if start is None else max(int(start), 1)
    if end is None:
        while True:
            for k in key_permution(seed, n_size):
                yield k, n_size
            n_size += 1
    else:
        end = int(end)
        while True:
            if n_size <= end:
                for k in key_permution(seed, n_size):
                    yield k, n_size
            else:
                return StopIteration()
            n_size += 1

async def guess_async_by_seed(path, min_length=None, max_length=None, seed=PWD_SEED_COMPLEX, progressbar=False):
    zfile = ZipFile(path)

    async def block(pwd):
        if try_open_zip(zfile, pwd):
            return pwd
        return False
    if progressbar: 
        with tqdm(key_generator(min_length, max_length, seed=seed)) as bar:
            async for pwd, _ in bar:
                if await block(pwd):
                    return pwd
    else:
        for pwd, _ in key_generator(min_length, max_length, seed=seed):
            if await block(pwd):
                return pwd
    return None

def guess_pwd_normal_by_seed(path, min_length=None, max_length=None, seed=PWD_SEED_COMPLEX, progressbar=False):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(guess_async_by_seed(path, min_length, max_length, seed, progressbar=progressbar))
    loop.run_until_complete(future)
    pwd = future.result()
    return pwd

def __guess_step(path, *pwds: bytes):
    zfile = ZipFile(path)
    for pwd in pwds:
        if try_open_zip(zfile, pwd):
            return pwd
    del pwds
    return False

def guess_in_multiprocess_by_seed(path, min_length=None, max_length=None, n_processes=8, slice_size=500, seed=PWD_SEED_COMPLEX, progressbar=False):
    pool = multiprocessing.Pool(n_processes)
    it = key_generator(min_length, max_length, seed=seed)
    manager = multiprocessing.Manager()
    info = manager.dict()
    info['key'] = None
    if progressbar:
        bar = tqdm(mininterval=0.25)
    def cb(re):
        if progressbar:
            bar.update(slice_size)
        if re:
            info['key'] = re
            pool.terminate()
    while True:
        try:
            pwds = itertools.islice(it, 0, slice_size)
            if pwds := list(pwds):
                pwds, char_sizes = list(zip(*pwds))
                char_size = char_sizes[-1]
                pool.apply_async(__guess_step, (path, *pwds), callback=cb, error_callback=print)
                del pwds
                del char_sizes
            else:
                pool.close()
                pool.join()
                pool.terminate()
                return info['key']
        except Exception as e:
            if e.args[0] == 'Pool not running':
                return info['key']
            else:
                raise e
        if progressbar:
            bar.set_postfix({
                "char": char_size
            }, refresh=False)
        gc.collect()

async def guess_async_by_book(path, book: list[bytes], progressbar=False):
    zfile = ZipFile(path)
    
    async def block(pwd):
        if try_open_zip(zfile, pwd):
            return pwd
        return False
    if progressbar:
        with tqdm(book) as bar:
            async for pwd in bar:
                if await block(pwd):
                    return pwd
    else:
        for pwd in book:
            if await block(pwd):
                return pwd
    return None

def guess_pwd_normal_by_book(path, book: list[bytes], progressbar=False):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(guess_async_by_book(path, book, progressbar=progressbar))
    loop.run_until_complete(future)
    pwd = future.result()
    return pwd

def __guess_step_by_book(path, pwd):
    zfile = ZipFile(path)
    if try_open_zip(zfile, pwd):
        return pwd
    return None

def guess_in_multiprocess_by_book(path, book:list, n_processes=8, chunksize=1000):
    pool = multiprocessing.Pool(n_processes)
    manager = multiprocessing.Manager()
    info = manager.dict()
    info['key'] = None
    sub_process =  partial(__guess_step_by_book, path)
    def cb(pwds):
        pwds = filter(None, pwds)
        for pwd in pwds:
            info['key'] = pwd
            pool.terminate()
            return
    pool.map_async(sub_process, book, chunksize=chunksize, callback=cb, error_callback=print)
    pool.close()
    pool.join()
    pool.terminate()
    return info['key']
        
class ZipCracker:

    def __init__(self, path) -> None:
        self.path = path

    def only_number(self, start=0, end=None, step=1, progressbar=False):
        return guess_number_pwd(self.path, start, end, step, progressbar)
    
    async def by_seed_async(self, seed=PWD_SEED_COMPLEX, min_length=None, max_length=None, progressbar=False):
        return await guess_async_by_seed(self.path, min_length, max_length, seed=seed, progressbar=progressbar)
    
    def by_seed(self, seed=PWD_SEED_COMPLEX, min_length=None, max_length=None, progressbar=False):
        return guess_pwd_normal_by_seed(self.path, min_length, max_length, seed=seed, progressbar=progressbar)
    
    def by_seed_mp(self, seed=PWD_SEED_COMPLEX, min_length=None, max_length=None, n_processes=None, slice_size=500, progressbar=False):
        return guess_in_multiprocess_by_seed(self.path, min_length, max_length, n_processes, slice_size, seed=seed, progressbar=progressbar)

    async def by_book_async(self, book: list[bytes], progressbar=False):
        return await guess_async_by_book(self.path, book, progressbar=progressbar)

    def by_book(self, book: list[bytes], progressbar=False):
        return guess_pwd_normal_by_book(self.path, book=book, progressbar=progressbar)
    
    def by_book_mp(self, book: list[bytes], n_processes=None, chunksize=1000):
        return guess_in_multiprocess_by_book(self.path, book=book, n_processes=n_processes, chunksize=chunksize)


if __name__ == '__main__':
    zguess = ZipCracker("./examples/data/flag.zip")
    # zguess = ZipCracker("./test/flag.zip")
    # pwd = zguess.by_seed_mp(slice_size=1000, progressbar=True, 
    #     seed=PWD_SEED_COMPLEX
    # )
    # pwd = zguess.by_seed(progressbar=True)
    # print(pwd)
    
    from codedict import Codes
    # k = zguess.by_book_mp(Codes.all_in().bytes())
    k = zguess.by_book_mp(Codes.all_in().bytes())
    # k  = zguess.only_number()
    print(k)