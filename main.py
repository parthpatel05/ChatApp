import socket
import os

# netstat -ano|findstr 55555
# taskkill /F /PID 12700

# start as soon as app starts
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 55555))
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
while True:
    #client, address = s.accept()
    print(address)
    client.send("you are now conneted ".encode())

    while True:
        message = input("enter the message: ")
        client.send(message.encode())

    client.close()
