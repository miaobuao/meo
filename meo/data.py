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


def load_file(path, encoding=None):
    '''read file auto-closed'''
    with open(path, 'rb') as _f:
        content = _f.read()

    if encoding:
        return content.decode(encoding=encoding)
    return content

def decode(_bytes: bytes):
    """decide encoding and decode `_bytes`"""
    assert isinstance(_bytes, bytes)
    for encoding in ["utf8", 'gbk', 'utf16', 'utf32']:
        try:
            return _bytes.decode(encoding)
        except: pass
