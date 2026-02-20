#!/usr/bin/python3
import socket, sys, os, fcntl, errno, struct
sys.path.append("/usr/lib")
from _kipr import *
PORT = 8080

SENSOR_LEFT = 0
SENSOR_RIGHT = 1
DISTANCE_SENSOR = 2
MOTOR_LEFT = 0
MOTOR_RIGHT = 1

SERVO_EXTENDER = 0
SERVO_ARM = 1
SERVO_CLAW = 2

BASE_SPEED = 100

ONE_METER_THRESHOLD = -9000

DEG_180_TIME = 2275

ARM_DOWN_POS = 923
ARM_UP_POS = 1800
CLAWS_OPEN_POS = 1000
CLAWS_CLOSE_POS = 2047
EXTENDER_HIGH_POS = 850
EXTENDER_LOW_POS = 1800

THRESHOLD = 2700

def is_white(sensor):
    return analog(sensor) < THRESHOLD

def is_black(sensor):
    return analog(sensor) >= THRESHOLD


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

def follow_line(base_speed):
    if is_white(SENSOR_LEFT) and is_white(SENSOR_RIGHT):
        forward(base_speed)
    elif is_white(SENSOR_LEFT) and is_black(SENSOR_RIGHT):
        turn_right(base_speed)
    elif is_black(SENSOR_LEFT) and is_white(SENSOR_RIGHT):
        turn_left(base_speed)
    else:
        forward(base_speed)

def follow_line_until_intersection(base_speed):
    while not is_black(SENSOR_LEFT) and not is_black(SENSOR_RIGHT):
        follow_line(base_speed)
        msleep(20)
    ao()
    msleep(10000)

def follow_line_2(base_speed):
    left_value = analog(SENSOR_LEFT)
    right_value = analog(SENSOR_RIGHT)
    error = left_value - right_value
    Kp = 0.10
    correction = int(Kp * error)
    left_speed = base_speed - correction
    right_speed = base_speed + correction
    left_speed = max(min(left_speed, 100), -100)
    right_speed = max(min(right_speed, 100), -100)
    xmotor(left_speed, right_speed)

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

def create_server():
    server_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_fd.bind(('', PORT))
    server_fd.listen(3)
    server_fd.setblocking(False)
    return server_fd

def connect_with(ip):
    client_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_fd.connect((ip, PORT))
    return client_fd

def accept_connections(server_fd):
    try:
        new_socket, _ = server_fd.accept()
        return new_socket
    except BlockingIOError:
        return -1

def send_message(new_socket, message):
    if new_socket != -1:
        new_socket.send(message.encode())

def get_message(new_socket):
    if new_socket != -1:
        return new_socket.recv(1024).decode()
    return None

def main():
    while True:
        forward(100)
    
main()
