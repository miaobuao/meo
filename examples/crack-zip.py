from meo.crack import Crack
from meo.utils import script_path
import meo
import os

path = os.path.join(script_path(__file__), "./data/flag.zip") # ./flag.zip
zguess = Crack.zip(path)

t, pwd = meo.wapper.timeit(
    lambda: zguess.in_multiprocess_by_seed()
)()
print(f"use {t}s -> {pwd}")

t, pwd = meo.wapper.timeit(
    lambda: zguess.by_seed()
)()
print(f"use {t}s -> {pwd}")
