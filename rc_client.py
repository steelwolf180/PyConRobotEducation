#remote controller client
import socket
import turtle

turtle.setup(500, 500, 0, 0)
IP = "192.168.#.#"
KEYPORT = 432
s = socket.socket()
s.connect((IP, KEYPORT))


def forward():
    s.send("w".encode())


def backward():
    s.send("s".encode())


def left():
    s.send("a".encode())


def right():
    s.send("d".encode())


def stop():
    s.send("q".encode())


turtle.onkeypress(forward, "w")
turtle.onkeypress(left, "a")
turtle.onkeypress(backward, "s")
turtle.onkeypress(right, "d")
turtle.onkeypress(stop, "q")
turtle.listen()
