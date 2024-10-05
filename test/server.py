import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())

s.bind((host, 4040))
s.listen()

cli, addr = s.accept()

def a():
    while 1:
        message = input("msg> ")
        cli.sendto(message.encode('ascii'), addr)
        print(addr)

def b():
    while 1:
        msg = cli.recv(1024).decode("ascii")
        if msg == "":pass
        else:print(msg)

th_a = threading.Thread(target=a)
th_b = threading.Thread(target=b)

th_a.start()
th_b.start()