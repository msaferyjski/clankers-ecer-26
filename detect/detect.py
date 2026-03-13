#!/usr/bin/python3
import cv2
import numpy as np

CAM_INDEX = 0
FRAME_W, FRAME_H = 640, 480
AREA_MIN = 2000

YELLOW_LOWER = np.array([20, 100, 100], dtype=np.uint8)
YELLOW_UPPER = np.array([30, 255, 255], dtype=np.uint8)

GREEN_LOWER = np.array([40, 70, 70], dtype=np.uint8)
GREEN_UPPER = np.array([80, 255, 255], dtype=np.uint8)

RED_LOWER1 = np.array([0, 150, 100], dtype=np.uint8)
RED_UPPER1 = np.array([10, 255, 255], dtype=np.uint8)
RED_LOWER2 = np.array([170, 150, 100], dtype=np.uint8)
RED_UPPER2 = np.array([180, 255, 255], dtype=np.uint8)

cap = cv2.VideoCapture(CAM_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)


def detect_and_draw(mask):
    direction = "N"

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    for cnt in contours:
        if cv2.contourArea(cnt) < AREA_MIN:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        center_x = x + w // 2

        third = FRAME_W // 3
        if center_x < third:
            direction = "L"
        elif center_x < 2 * third:
            direction = "Z"
        elif center_x > 2 * third:
            direction = "R"
        else:
            direction = "N"

    return direction

def get_direction_and_frame(farbe):
    ok, frame = cap.read()
    if not ok:
        return "N", None

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_yellow = cv2.inRange(hsv, YELLOW_LOWER, YELLOW_UPPER)
    mask_green = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)
    mask_r1 = cv2.inRange(hsv, RED_LOWER1, RED_UPPER1)
    mask_r2 = cv2.inRange(hsv, RED_LOWER2, RED_UPPER2)
    mask_red = cv2.bitwise_or(mask_r1, mask_r2)

    if farbe == "Gelb":
        direction = detect_and_draw(mask_yellow)
    if farbe == "Gruen":
        direction = detect_and_draw(mask_green)
    if farbe == "Rot":
        direction = detect_and_draw(mask_red)

    return direction, frame

def get_direction(farbe):
    direction, _ = get_direction_and_frame(farbe)
    return direction