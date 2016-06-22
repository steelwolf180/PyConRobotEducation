# remote controller server
import socket
import threading

import pi2go

pi2go.init()

KEYPORT = 432
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
s.bind(("", KEYPORT))
s.listen(0)


def handle_connection(c):
    while True:
        data = c.recv(1).decode()
        if data == "l":
            robot_line()
        else:
            break
    c.close()


def keypress_server():
    while True:
        conn, addr = s.accept()
        print("Keypress connection from " + addr[0])
        handle_connection(conn)
        print("Keypress connection closed")


# Here we set the speed to 60 out of 100 - feel free to change!
speed = 60


def robot_line():
    try:
        while True:
            # Defining the sensors on the bottom of the Pi2Go
            left = pi2go.irLeftLine()
            right = pi2go.irRightLine()
            if left == right:  # If both sensors are the same (either on or off):
                # Forward
                pi2go.forward(speed)
            elif left == True:  # If the left sensor is on
                # Left
                pi2go.spinRight(speed)
            elif right == True:  # If the right sensor is on
                # Right
                pi2go.spinLeft(speed)

    finally:  # Even if there was an error, cleanup
        pi2go.cleanup()


threading.Thread(target=keypress_server).start()
