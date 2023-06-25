from test_imp import meo
import os

zip_path = os.path.join(meo.utils.script_path(__file__), "../examples/data/flag.zip")

def test_zip_crack():
    zc = meo.crack.Crack.zip(zip_path)
    real_pwd = b'a4c'
    assert zc.by_seed(meo.crack.utils.PWD_SEED_SIMPLE) == real_pwd
    assert zc.in_multiprocess_by_seed(meo.crack.utils.PWD_SEED_SIMPLE) == real_pwd