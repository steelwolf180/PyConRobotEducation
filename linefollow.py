from random import randint
from time import sleep

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

for motorpin in [26, 24, 19, 21]:
    GPIO.setup(motorpin, GPIO.OUT)

lineleft = 12
lineright = 15
infront = 13

for pin in [lineleft, lineright, infront]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lefta = GPIO.PWM(26, 20)
leftb = GPIO.PWM(24, 20)
righta = GPIO.PWM(19, 20)
rightb = GPIO.PWM(21, 20)

lefta.start(0)
leftb.start(0)
righta.start(0)
rightb.start(0)


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


def vertical(speed):
    left(speed)
    right(speed)


def leftIsBlack():
    return GPIO.input(lineleft) == 1


def rightIsBlack():
    return GPIO.input(lineright) == 1


def thingInFront():
    return GPIO.input(infront) == 0


try:
    while True:
        sleep(0.01)
        if not leftIsBlack() and not rightIsBlack():
            left(50)
            right(-20)
        elif leftIsBlack():
            left(-20)
            right(50)
        else:
            vertical(50)
        if thingInFront():
            vertical(-50)
            sleep(1)
            vertical(0)
            if randint(0, 1) == 1:
                left(50)
            else:
                right(50)
            sleep(1)
            vertical(50)



        ##    shouldMoveLeft = False
        ##    shouldMoveRight = False
        ##    while True:
        ##        if GPIO.input(lineleft) == 0:
        ##            print("go left")
        ##        if GPIO.input(lineright) == 0:
        ##            print("go right")
        ##        sleep(0.1)
        ##
        ##        if GPIO.input(lineleft) != GPIO.input(lineright):
        ##            straight(35)
        ##            shouldMoveLeft = False
        ##            shouldMoveRight = False
        ##
        ##        elif shouldMoveLeft:
        ##            right(0)
        ##            left(35)
        ##            print("Moving left")
        ##
        ##        elif shouldMoveRight:
        ##            left(0)
        ##            right(35)
        ##            print("Moving right")
        ##
        ##        elif GPIO.input(lineleft) == 1 and GPIO.input(lineright) == 1:
        ##            right(0)
        ##            left(35)
        ##            print("Moving left")
        ##            sleep(1)
        ##            shouldMoveLeft = False
        ##            shouldMoveRight = False
        ##            if GPIO.input(lineleft) == 1 and GPIO.input(lineright) == 1:
        ##                shouldMoveRight = True
        ##
        ##        elif GPIO.input(lineright) == 0 and GPIO.input(lineleft) == 0:
        ##            left(0)
        ##            right(35)
        ##            print("Moving right")
        ##            sleep(1)
        ##            shouldMoveLeft = False
        ##            shouldMoveRight = False
        ##            if GPIO.input(lineleft) == 0 and GPIO.input(lineright) == 0:
        ##                shouldMoveLeft = True

        # elif GPIO.input(lineright) == GPIO.input(lineleft):
##        else:
##            straight(35)
##            shouldMoveLeft = False
##            shouldMoveRight = False
except KeyboardInterrupt:
    GPIO.cleanup()
