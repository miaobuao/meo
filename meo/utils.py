"""
    awesome functions
"""
import os

def script_path(__file__):
    """return script real path in disk."""
    return os.path.split(os.path.realpath(__file__))[0]
