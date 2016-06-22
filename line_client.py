#line sensor client
import socket
import turtle

turtle.setup(500, 500, 0, 0)
IP = "192.168.#.#"
KEYPORT = 432
s = socket.socket()
s.connect((IP, KEYPORT))


def linefollowing():
    s.send("l".encode())

turtle.onkeypress(linefollowing(), "l")
turtle.listen()
