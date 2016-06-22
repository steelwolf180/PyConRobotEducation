#avoider client

import socket
import turtle

turtle.setup(500, 500, 0, 0)
IP = "192.168.#.#"
KEYPORT = 432
s = socket.socket()
s.connect((IP, KEYPORT))


def avoider():
    s.send("o".encode())


turtle.onkeypress(avoider(), "o")
turtle.listen()
