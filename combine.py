import cv2
import numpy as np

def pick_circle():
    print("pick up")
    # from adafruit_servokit import ServoKit
    #
    # import time
    # import board
    # import busio
    #
    # i2c_bus0 = busio.I2C(board.SCL_1, board.SDA_1)
    # kit = ServoKit(channels=16, i2c=i2c_bus0)
    #
    # kit.servo[0].angle = 130
    #
    # kit.servo[1].angle = 170
    #
    # kit.servo[2].angle = 20
    #
    # kit.servo[3].angle = 130
    #
    # kit.servo[4].angle = 0
    #
    # kit.servo[5].angle = 20
    #
    # # Pick
    #
    # for i in range(130, 30, -1):
    #     kit.servo[0].angle = i
    #
    # for i in range(170, 100, -1):
    #     kit.servo[1].angle = i
    #     time.sleep(.01)
    #
    # time.sleep(.51)
    #
    # for i in range(20, 56, 1):
    #     kit.servo[5].angle = i
    #     time.sleep(.01)
    # time.sleep(.51)
    #
    # # place
    # for i in range(100, 170, 1):
    #     kit.servo[1].angle = i
    #     time.sleep(.01)
    #
    # for i in range(30, 130, 1):
    #     kit.servo[0].angle = i
    #     time.sleep(.01)
    #
    # # SORTING AFTER PICKNG
    #
    # for i in range(170, 100, -1):
    #     kit.servo[1].angle = i
    #     time.sleep(.01)
    #
    # for i in range(53, 20, -1):
    #     kit.servo[5].angle = i
    #     time.sleep(.01)
    #
    # for i in range(100, 170, 1):
    #     kit.servo[1].angle = i
    #     time.sleep(.01)

def circle(frame):
    # Convert to grayscale.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=1,
                                        maxRadius=40)
    # Draw circles that are detected.
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            temp = [a, b]
            # Draw the circumference of the circle.
            txt = 'Circle location: ' + str(a) + ', ' + str(b)
            frame = cv2.putText(frame, txt, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
            cv2.circle(frame, (a, b), r, (0, 255, 0), 2)
            # # Draw a small circle (of radius 1) to show the center.
            cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)
        pick_circle()
    return frame

def square(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

    thresh = cv2.threshold(sharpen, 200, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    min_area = 100
    max_area = 1500
    image_number = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_area and area < max_area:
            x, y, w, h = cv2.boundingRect(c)
            ROI = frame[y:y + h, x:x + h]
            txt = 'Square location: ' + str(x) + ', ' + str(y)
            frame = cv2.putText(frame, txt, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
            xCenter = round((w / 2) + x)
            yCenter = round((h / 2) + y)
            frame = cv2.circle(frame, (xCenter, yCenter), 2, (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 2)
    return frame

cam = cv2.VideoCapture(1)

while True:
    ret, frame = cam.read()
    frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
    frame = circle(frame)
    frame = square(frame)
    cv2.rectangle(frame, (0, 0), (480, 640), (0, 255, 0), 2)
    cv2.rectangle(frame, (30, 130), (450, 554), (255, 0, 0), 2)
    cv2.rectangle(frame, (0, 28), (480, 570), (0, 0, 255), 2)
    cv2.imshow("frame", frame)
    cv2.waitKey(1)