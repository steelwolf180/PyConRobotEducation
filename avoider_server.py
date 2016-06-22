#avoider server
import pi2go
import socket
import threading
import time

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
        if data == "o":
            avoider()
        else:
            break
    c.close()


def avoider_server():
    while True:
        conn, addr = s.accept()
        print("Keypress connection from " + addr[0])
        handle_connection(conn)
        print("Keypress connection closed")

speed = 40


def avoider():
    try:
        while True:
            if pi2go.irLeft():
                while pi2go.irLeft():
                    # While the left sensor detects something - spin right
                    pi2go.spinRight(speed)
                pi2go.stop()
            if pi2go.irRight():
                while pi2go.irRight():
                    # While the right sensor detects something - spin left
                    pi2go.spinLeft(speed)
                pi2go.stop()
            while not (pi2go.irLeft() or pi2go.irRight()):
                if pi2go.getDistance() <= 0.3:  # If the distance is less than 0.3, spin right for 1 second
                    pi2go.spinRight(speed)
                    time.sleep(1)
                else:
                    pi2go.forward(speed)
            pi2go.stop()

    finally:  # Even if there was an error, cleanup
        pi2go.cleanup()


threading.Thread(target=avoider_server).start()
