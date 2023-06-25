import multiprocessing
import gc
from .utils import *
from tqdm.asyncio import tqdm
import itertools
import asyncio

class Cracker:
    
    def __init__(self, path: str) -> None:
        self.path = path

    def in_multiprocess_by_seed(self, seed=PWD_SEED_COMPLEX, min_length=None, max_length=None, n_processes=8, slice_size=500, progressbar=False):
        pool = multiprocessing.Pool(n_processes)
        it = key_generator(seed, min_length, max_length)
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
                    pool.apply_async(self.step_some, (*pwds, ), callback=cb, error_callback=print)
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

    def in_multiprocess_by_book(self, book:list, n_processes=8, chunksize=1000):
        pool = multiprocessing.Pool(n_processes)
        manager = multiprocessing.Manager()
        info = manager.dict()
        info['key'] = None
        def cb(pwds):
            pwds = filter(None, pwds)
            for pwd in pwds:
                info['key'] = pwd
                pool.terminate()
                return
        pool.map_async(self.step_once, book, chunksize=chunksize, callback=cb, error_callback=print)
        pool.close()
        pool.join()
        pool.terminate()
        return info['key']
    
    def step_once(self, pwd: bytes) -> None | bytes: pass
    def step_some(self, *pwd: bytes) -> None | bytes: pass
        
    def only_number(self, start=0, end=None, step=1, progressbar=False):
        start = int(start)
        if end is None:
            now = start
            while True:
                pwd = str(now).encode("utf8")
                if self.step_once(pwd):
                    return pwd
                now += step
        end = int(end)
        bar = range(start, end, step)
        if progressbar:
            bar = tqdm(bar)
        for number in bar:
            pwd = str(number).encode("utf8")
            if self.step_once(pwd):
                return pwd
        return None
    
    async def by_seed_async(self, seed=PWD_SEED_COMPLEX, min_length=None, max_length=None, progressbar=False):
        async def block(pwd):
            if self.step_once(pwd):
                return pwd
            return False
        if progressbar: 
            with tqdm(key_generator(seed, min_length, max_length)) as bar:
                async for pwd, _ in bar:
                    if await block(pwd):
                        return pwd
        else:
            for pwd, _ in key_generator(seed, min_length, max_length):
                if await block(pwd):
                    return pwd
        return None

    def by_seed(self, seed=PWD_SEED_COMPLEX, min_length=None, max_length=None, progressbar=False):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.by_seed_async(seed=seed, min_length=min_length, max_length=max_length, progressbar=progressbar))
        loop.run_until_complete(future)
        pwd = future.result()
        return pwd

    async def by_book_async(self, book: list[bytes], progressbar=False):
        async def block(pwd):
            if self.step_once(pwd):
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

    def by_book(self, book: list[bytes], progressbar=False):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.by_book_async(book, progressbar=progressbar))
        loop.run_until_complete(future)
        pwd = future.result()
        return pwd