import socket
from threading import Thread
import random
from datetime import datetime
from colorama import Fore, init, Back
import time

init()  # initialize colorama

#set available colors
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

#choose a random color for the client
color = random.choice(colors)

#server's IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

# create a TCP socket
s = socket.socket()
print(f"{color}[+] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print(f"{color}[+] Connected.")

# get the client's name
name = input("Enter your name: ")

# a thread to listen for incoming messages
def receive_messages():
    while True:
        try:
            # receive 1024 bytes of data from the server
            # if the size is more than 1024 bytes, it will be split into multiple messages
            message = s.recv(1024).decode()
            if message == 'NAME':
                # if the server sends 'NAME' it means we need to send our name
                s.send(name.encode())
            else:
                # if the server sends anything other than 'NAME' we print the message
                print(message)
        except:
            # if an error occurs, we print it and break out of the loop
            print(f"{color}[!] Error!")
            s.close()
            break

# start the receive_messages thread
t = Thread(target=receive_messages)
t.daemon = True
t.start()

# loop to send messages to the server
while True:
    # get the message from the user
    message = input(f"{color}{name} > ")
    # if the message is not empty - send it
    if message:
        # send the message to the server
        s.send(f"{message}{separator_token}".encode())

# close the socket
s.close()
