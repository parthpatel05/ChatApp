import socket
import os
import threading

# netstat -ano|findstr 55555
# taskkill /F /PID 12700

# start as soon as app starts, to pick the connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # sender
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # reciever

def zeroOneChoice(prompt):
    while True:
        try:
            choice = int(input(prompt))
            if choice != 0 and choice != 1:
                raise Exception

            return choice
        except:
            print("Please enter a 0 or 1")


connectionChoice = zeroOneChoice("Would you like to connect(0) or wait for a connection(1): ")
if connectionChoice == 0:
            otherIp = input('please enter the other ip: ')

            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((otherIp, 55555))

            # recieve the connection, making sender socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)

            r.bind((local_ip, 55556))
            r.listen()

            # conecting to a specific client
            client_acquired = False
            while not client_acquired:
                client, address = r.accept()
                if len(address) > 0:
                    if address[0] == otherIp:
                        client_acquired = True

elif connectionChoice == 1:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(local_ip)

            # recieve the connection, making sender socket
            r.bind((local_ip, 55555))
            r.listen()
            print("listening: ...")

            # conecting to a specific client
            client_acquired = False
            while not client_acquired:
                client, address = r.accept()
                if len(address) > 0:
                    print("This person is trying to connect to you")
                    print(address)
                    choice = input("If you would like to accept (1), else (0): ")
                    if int(choice) == 1:
                        client_acquired = True

            # sending a request for connection, making reciever socket
            s.connect((address[0], 55556))



# sending message
def sender():
    while True:
        #print(address)
        client.send("you are now conneted ".encode())
        endConnection = False
        while not endConnection:
            message = input("enter the message (~ will close the connection): ")
            if message == "~":
                endConnection = True
            client.send(message.encode())

        client.close()
        print("-!-!-!-connection ended-!-!-!-")
        break


t1 = threading.Thread(target=sender)
t1.start()
t1.join()
