import socket
import os
import threading

# netstat -ano|findstr 55555
# taskkill /F /PID 12700

# start as soon as app starts
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind(("127.0.0.1", 55555))
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(local_ip)
s.bind((local_ip, 55555))
s.listen()
print("listening: ...")

# conecting to a specific client
client_acquired = False
while not client_acquired:
    client, address = s.accept()
    if len(address) > 0:
        print("This person is trying to connect to you")
        print(address)
        choice = input("If you would like to accept (1), else (0): ")
        if int(choice) == 1:
            client_acquired = True

# sending message
def sender():
    while True:
        #client, address = s.accept()
        print(address)
        client.send("you are now conneted ".encode())
        endConnection = False
        while not endConnection:
            message = input("enter the message (~ will close the connection): ")
            if message == "~":
                endConnection = True
            client.send(message.encode())

        client.close()
        break

t1 = threading.Thread(target=sender)
t1.start()
t1.join()