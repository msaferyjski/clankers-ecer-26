#!/usr/bin/python3
import sys
sys.path.append("/usr/lib")
sys.path.append("/home/kipr/src/modules")
from _kipr import *

from move import *

def main():
    while True:
        move_for_m(5, 100, forward)
    
main()
