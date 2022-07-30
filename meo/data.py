""" IO of formatted file and object """
import json


def load_json(path: str):
    """ load json file from ```path``` """
    with open(path, 'rb') as _f:
        return json.load(_f)

def to_json(obj, path: str, encoding='utf8', ensure_ascii=False, indent=None):
    """ Serialize obj as a JSON formatted stream to ```path```` """
    with open(path, 'w+', encoding=encoding) as _f:
        json.dump(obj, _f, ensure_ascii=ensure_ascii, indent=indent)


def read_file(path, mode='r', encoding='utf8'):
    '''read file auto-closed'''
    if 'b' in mode:
        with open(path, mode) as _f:
            return _f.read()
    else:
        with open(path, mode, encoding) as _f:
            return _f.read()
