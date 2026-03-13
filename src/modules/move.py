from _kipr import *

MOTOR_LEFT = 0
MOTOR_RIGHT = 1
DEG_180_TIME = 2275
ONE_METER_THRESHOLD = -9000

def xmotor(left_speed, right_speed):
    motor(MOTOR_LEFT, left_speed)
    motor(MOTOR_RIGHT, right_speed)

def xmav(left_speed, right_speed):
    mav(MOTOR_LEFT, left_speed)
    mav(MOTOR_RIGHT, right_speed)

def forward(base_speed):
    xmotor(base_speed, base_speed)

def turn_right(base_speed):
    xmotor(base_speed // 2, -base_speed)

def turn_left(base_speed):
    xmotor(-base_speed, base_speed // 2)

def turn_deg(deg):
    deg_1_time = (DEG_180_TIME * 2) / 360
    if deg < 0:
        turn_right(100)
    else:
        turn_left(100)
    msleep(int(deg_1_time * abs(deg)))
    ao()

def turn_around():
    turn_deg(180)

def move_for_m(m, base_speed, moveFn):
    cmpc(MOTOR_LEFT)
    cmpc(MOTOR_RIGHT)
    pc = (m * ONE_METER_THRESHOLD) * 0.95
    while gmpc(MOTOR_LEFT) > pc or gmpc(MOTOR_RIGHT) > pc:
        moveFn(base_speed)
    ao()

def move_until_distance_sensor(sensor_value, base_speed, moveFn):
    while analog(DISTANCE_SENSOR) < sensor_value:
        moveFn(base_speed)
    ao()

def move_for_cm(cm, base_speed, moveFn):
    move_for_m(cm * -0.01, base_speed, moveFn)