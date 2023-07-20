"""
    awesome functions
"""
import os

def script_path(__file__):
    """return script real path in disk."""
    return os.path.split(os.path.realpath(__file__))[0]

class SimplePath:
    def __init__(self, path: str) -> None:
        self.path = path

    def join(self, *paths):
        path = os.path.join(self.path, *paths)
        return SimplePath(path)

def ScriptPath(__file__):
    return SimplePath(script_path(__file__))
