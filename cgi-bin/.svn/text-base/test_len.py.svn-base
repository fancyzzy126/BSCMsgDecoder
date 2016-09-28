#!/usr/bin/python
import sys

def test_len(filename):
    fd = file(filename)
    content = fd.readlines()
    n = 1024
    re = [0]
    while len(re) > 0:
        re = [it for it in content if len(it) > n]
        n = n << 1
    print n>>11
if __name__ == '__main__':
    test_len(sys.argv[1])
