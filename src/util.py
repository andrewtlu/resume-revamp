import os

def from_base_path(path):
    filepath = os.path.dirname(__file__)
    return os.path.abspath(filepath + os.sep + os.pardir + os.sep + path)