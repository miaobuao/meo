from meo.crack import Crack
from meo.utils import script_path
import os

path = os.path.join(script_path(__file__), "./data/flag.zip") # ./flag.zip
zguess = Crack.zip(path)
pwd = zguess.by_seed_mp()
print(pwd)
