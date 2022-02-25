from os.path import dirname, basename, isfile, join
from .mongoDB import mongoDB
from algo_model import *
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
# print(__all__)