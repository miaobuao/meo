""" IO of formatted file and object """
import json5
import json
import os

def checkout_dir(dir_path):
    """Create if the folder does not exist"""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def checkout_file_path(path):
    fdir, _ = os.path.split(path)
    checkout_dir(fdir)

def to_json5(obj, path: str, encoding='utf8', ensure_ascii=False, indent=None, auto_mkdirs=True):
    if auto_mkdirs:
        checkout_file_path(path)
    with open(path, 'w+', encoding=encoding) as _f:
        json5.dump(obj, _f, ensure_ascii=ensure_ascii, indent=indent)

def load_json5(path: str):
    with open(path, 'rb') as _f:
        return json5.load(_f)

def to_json(obj, path: str, encoding='utf8', ensure_ascii=False, indent=None, auto_mkdirs=True):
    """ Serialize obj as a JSON formatted stream to ```path```` """
    if auto_mkdirs:
        checkout_file_path(path)
    with open(path, 'w+', encoding=encoding) as _f:
        json.dump(obj, _f, ensure_ascii=ensure_ascii, indent=indent)

def load_json(path: str):
    """ load json file from ```path``` """
    with open(path, 'rb') as _f:
        return json.load(_f)

def to_file(path, data, mode='w+', encoding=..., auto_mkdirs=True):
    """write file and auto create dir not existed """
    if auto_mkdirs:
        checkout_file_path(path)
    if 'b' in mode:
        if encoding is ...:
            encoding = None
    elif encoding is ...:
        encoding = 'utf8'
    with open(path, mode, encoding=encoding) as _f:
        return _f.write(data)

def load_file(path, encoding=None):
    '''read file auto-closed'''
    with open(path, 'rb') as _f:
        content = _f.read()
    if encoding is None:
        return content
    return content.decode(encoding=encoding)

def decode(_bytes: bytes):
    """decide encoding and decode `_bytes`"""
    assert isinstance(_bytes, bytes)
    for encoding in ["utf8", 'gbk', 'utf16', 'utf32']:
        try:
            return _bytes.decode(encoding)
        except: pass
    raise ValueError("bytes must be {utf8, gbk, utf16, utf32}")

def encode(string: str):
    assert isinstance(string, str)
    for enc in ["utf8", 'gbk', 'utf16', 'utf32']:
        try:
            return string.encode(enc)
        except: pass
    raise ValueError("bytes must be {utf8, gbk, utf16, utf32}")


def cat(*path):
    file_bytes = bytes()
    for p in path:
        if os.path.isfile(p):
            file_bytes += load_file(p)
        else:
            raise ValueError(f"{p} is not a file")
    return file_bytes

if __name__ == '__main__':
    data = {
        "test": 111
    }
    to_json(data, "./test/output.json")
    to_json5(data, "./test/output.json5")