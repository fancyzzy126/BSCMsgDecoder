#!/usr/bin/python

import os, re
from time import *

__debug = 0 and True or False;

def is_debug():
    return __debug;

def set_debug(flag):
    __debug = flag;

def debug_print(text, btime = True):
    if not is_debug():
        return;
    if (btime):
        print asctime() + ' ' + str(text);
    else:
        print text;

if __name__ == '__main__':
    print("is_debug: %d"%is_debug());
    debug_print("Hello debug trace.", False);
    debug_print("Hello debug trace with timestamp.");

