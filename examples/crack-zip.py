from meo.crack import Crack
from meo.utils import script_path
import os

path = os.path.join(script_path(__file__), "./data/flag.zip") # ./flag.zip
zguess = Crack.zip(path)
pwd = zguess.in_multiprocess_by_seed(progressbar=True)
print(pwd)