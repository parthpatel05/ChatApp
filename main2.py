import socket
import os
import threading

# connecting/ file
otherIp = input('please enter the other ip: ')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(('127.0.0.1', 55555))
#s.connect(("104.194.100.190", 55555))
s.connect((otherIp, 55555))
file = open("chat.txt", 'a')
file.write("new chat starting \n")

def recieveer():
    end_connection = False
    while not end_connection:
        message = s.recv(1024).decode()
        if len(message) > 0:
            file.write(message+"\n")
            print(message)
        else:  # if conection closed
            end_connection = True
            print("-!-!-!-connection ended-!-!-!-")


t1 = threading.Thread(target=recieveer)
t1.start()
t1.join()

s.close() # closing socket, will need to make a function cuz we will close 2 sockets

# todo how to make them seperate apps
