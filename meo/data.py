""" IO of formatted file and object """
import json
import os


def checkout_dir(dir_path):
    """Create if the folder does not exist"""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def _checkout_file_path(path):
    fdir, _ = os.path.split(path)
    checkout_dir(fdir)


def to_json(obj, path: str, encoding='utf8', ensure_ascii=False, indent=None, auto_mkdirs=True):
    """ Serialize obj as a JSON formatted stream to ```path```` """
    if auto_mkdirs:
        _checkout_file_path(path)
    with open(path, 'w+', encoding=encoding) as _f:
        json.dump(obj, _f, ensure_ascii=ensure_ascii, indent=indent)


def to_file(path, data, mode='w+', encoding="utf8", auto_mkdirs=True):
    """write file and auto create dir not existed """
    if auto_mkdirs:
        _checkout_file_path(path)
    with open(path, mode, encoding=encoding) as _f:
        return _f.write(data)


def load_json(path: str):
    """ load json file from ```path``` """
    with open(path, 'rb') as _f:
        return json.load(_f)


def read_file(path, mode='r', encoding='utf8'):
    '''read file auto-closed'''
    if 'b' in mode:
        with open(path, mode) as _f:
            return _f.read()
    else:
        with open(path, mode, encoding) as _f:
            return _f.read()
