import move

SENSOR_LEFT = 0
SENSOR_RIGHT = 1

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