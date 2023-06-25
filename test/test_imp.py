import sys
import os
script_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(0, os.path.join(script_path, ".."))

import meo