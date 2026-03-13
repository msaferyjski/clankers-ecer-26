from _kipr import *

ARM_DOWN_POS = 923
ARM_UP_POS = 1800
CLAWS_OPEN_POS = 1000
CLAWS_CLOSE_POS = 2047
EXTENDER_HIGH_POS = 850
EXTENDER_LOW_POS = 1800

SERVO_EXTENDER = 0
SERVO_ARM = 1
SERVO_CLAW = 2

def set_servo_position_gradual(port, goal):
    curr_pos = get_servo_position(port)
    if curr_pos < goal:
        for i in range(curr_pos, goal):
            set_servo_position(port, i)
            msleep(1)
    elif curr_pos > goal:
        for i in range(curr_pos, goal, -1):
            set_servo_position(port, i)
            msleep(1)

def extender_up():
    set_servo_position_gradual(SERVO_EXTENDER, EXTENDER_HIGH_POS)

def extender_down():
    set_servo_position_gradual(SERVO_EXTENDER, EXTENDER_LOW_POS)

def lower_arm():
    set_servo_position_gradual(SERVO_ARM, ARM_DOWN_POS)

def lift_arm():
    set_servo_position_gradual(SERVO_ARM, ARM_UP_POS)

def open_claw():
    set_servo_position_gradual(SERVO_CLAW, CLAWS_OPEN_POS)

def close_claw():
    set_servo_position_gradual(SERVO_CLAW, CLAWS_CLOSE_POS)

def start_servos():
    enable_servos()
    extender_up()
    lift_arm()
    open_claw()