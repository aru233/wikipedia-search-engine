import sys
import os

from .parser import Parser

if __name__ == '__main__':
    filename = sys.argv[1]
    parser = Parser(filename)
