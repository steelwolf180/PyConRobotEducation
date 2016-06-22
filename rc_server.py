#remote controller server
import socket
import threading

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

lineRight = 13
lineLeft = 12
for motorpin in [26, 24, 19, 21]:
    GPIO.setup(motorpin, GPIO.OUT)

lefta = GPIO.PWM(26, 20)
leftb = GPIO.PWM(24, 20)
righta = GPIO.PWM(19, 20)
rightb = GPIO.PWM(21, 20)

KEYPORT = 432
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
s.bind(("", KEYPORT))
s.listen(0)

def handle_connection(c):
    while True:
        data = c.recv(1).decode()
        if data == "w":
            left(100)
            right(100)
        elif data == "s":
            left(-100)
            right(-100)
        elif data == "a":
            left(-100)
            right(100)
        elif data == "d":
            left(100)
            right(-100)
        elif data == "q":
            left(0)
            right(0)
        else:
            break
    c.close()


def keypress_server():
    while True:
        conn, addr = s.accept()
        print("Keypress connection from " + addr[0])
        handle_connection(conn)
        print("Keypress connection closed")


def left(speed):
    if speed > 0:
        speed = min(speed, 100)
        leftb.ChangeDutyCycle(0)
        lefta.ChangeDutyCycle(speed)
    elif speed < 0:
        speed = max(speed, -100)
        lefta.ChangeDutyCycle(0)
        leftb.ChangeDutyCycle(abs(speed))
    else:
        lefta.ChangeDutyCycle(0)
        leftb.ChangeDutyCycle(0)


def right(speed):
    if speed > 0:
        speed = min(speed, 100)
        rightb.ChangeDutyCycle(0)
        righta.ChangeDutyCycle(speed)
    elif speed < 0:
        speed = max(speed, -100)
        righta.ChangeDutyCycle(0)
        rightb.ChangeDutyCycle(abs(speed))
    else:
        righta.ChangeDutyCycle(0)
        rightb.ChangeDutyCycle(0)

lefta.start(0)
leftb.start(0)
righta.start(0)
rightb.start(0)

threading.Thread(target=keypress_server).start()
