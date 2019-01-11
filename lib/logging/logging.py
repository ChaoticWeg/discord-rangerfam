from os import path
import logging

_instance = None

def __get_logfile(filename):
    return path.join(path.dirname(path.realpath(__file__)), filename)

def __create_logger():
    result = logging.getLogger('wegbot')
    result.setLevel(logging.DEBUG)

    fh = logging.FileHandler(__get_logfile('wegbot.log'))
    fh.setLevel(logging.DEBUG)
    result.addHandler(fh)

    return result

def get_logger():
    global _instance

    if _instance is None:
        _instance = __create_logger()

    return _instance
