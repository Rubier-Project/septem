import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())

s.connect((host, 4040))

while 1:
    msg = s.recv(1024).decode('ascii').strip()

    if not msg == "":
        if msg == "hi":
            s.sendto("Hiii".encode("ascii"), (host, 4040))
