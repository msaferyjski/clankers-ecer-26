from _kipr import *

THRESHOLD = 2700

def is_white(sensor):
    return analog(sensor) < THRESHOLD

def is_black(sensor):
    return analog(sensor) >= THRESHOLD