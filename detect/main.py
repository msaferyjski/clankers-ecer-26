#!/usr/bin/python3
import os, sys
sys.path.append("/usr/lib")
import _kipr as k
import detect

def main():
    while True:
        d = detect.get_direction("Gruen")
        if d == "Z":
            k.motor(0, 100) #Links vorne
            k.motor(1, -100) #Rechts vorne
            k.motor(2, -100) #Links hinten
            k.motor(3, 100) #Rechts hinten
        elif d == "L":
            k.motor(0, -100)
            k.motor(1, -100)
            k.motor(2, 100)
            k.motor(3, 100)
        elif d == "R":
            k.motor(0, 100)
            k.motor(1, 100)
            k.motor(2, -100)
            k.motor(3, -100)
        else:
            k.motor(0, 100)
            k.motor(1, 100)
            k.motor(2, -100)
            k.motor(3, -100)
        print(d, flush=True)

main()