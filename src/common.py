import sys, os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path) #type: ignore
    return os.path.join(os.path.abspath("."), relative_path)