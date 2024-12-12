# TASK 1: DNS-related commands
# TASK 2: HTTP, FTP

# TASK 4: Basic Socket programming

import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import *
import requests # for HTTP requests
import ftplib # for FTP connection
from ftplib import FTP
import socket # for error handling
from time import sleep
import socket
import threading
import time

# initializing server UDP
server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_udp.bind(('localhost', 12346))

# function to send message
def send_msg_tcp(message):
    client_tcp.send(message.encode('utf-8'))

# thread will be created on that function to receive message
def handle_client(client):
    while True:
        message = client.recv(4096)
        if not message:
            print("Message is empty!")
            break
        decoded_message = message.decode('utf-8')
        print("Server received some message from client: ")
        print(decoded_message)
        # echo the message to test connection
        client.send(message)

    client.close()

# TCP server initializing function
def server():
    ip_address = 'localhost'
    port = 12345
    server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_tcp.bind((ip_address, port))
    server_tcp.listen()

    while True:
        client, address = server_tcp.accept()
        print("Accepting connection")
        client_thread = threading.Thread(
                    target=handle_client,
                    args=(client,)
        )
        client_thread.start()

server_thread = threading.Thread(target=server)
server_thread.start()

def server_udp_start():
    while True:
        message, address = server_udp.recvfrom(4096)
        print("Server: message from client: ")
        print(message.decode('utf-8'))
    server_udp.close()

# UDP server initializing function
def send_msg_udp(message):
    address = ('localhost', 12346)
    client_udp.sendto(message.encode('utf-8'), address)

# main function to ask on which functionality user would like to work on
while True:
    print("Choose DNS command or Protocol or Socket to work with: nslookup, dig, host, http, ftp, socket ")
    option = input()

    if (option.lower() == 'nslookup'):
        address = input("Please, enter domain name: ")
        result_command = subprocess.run(["nslookup", address], capture_output=True, text = True) # subprocess.run() to execute the command, capture_output is True to print text of object later
        print(result_command.stdout)

    if (option.lower() == 'dig'):
        address = input("Please, enter domain name: ")
        result_command1 = subprocess.run(["dig", address], capture_output=True)
        print(result_command1.stdout)

    if (option.lower() == 'host'):
        address = input("Please, enter domain name: ")
        result_command2 = subprocess.run(["host", address], capture_output=True)
        print(result_command2.stdout)

    if (option.lower() == 'http'):
        print("Making HTTP Get request...")
        server = input("Target server: ") # getting input from user
        port = input("Target port (usually 80): ")
        http = "http://"
        separator = ":"
        if not server or not port:
            print("Empty!")
        else:
            url = f"{http}{server}{separator}{port}" # making an url to do get request on http
            params = None
            request = requests.get(url, params = params)
            print(request.text) # printing text of this request object

    # for FTP connection establishing scenario
    if (option.lower() == 'ftp'):
        print("Making FTP Connection...")
        host = input("Target host: ")
        user = "demo"
        password = "password" # set to this values of 'test.rebex.net' ftp server
        try:
            print("Connecting to the FTP server...")
            ftp_obj = FTP()
            with ftp_obj as ftp:
                ftp.connect(host, port=21) # default port was set
                ftp.login(user = user, passwd = password)
                print("Successful connection!")
                sleep(2)
            print("Closing the connection...")
        except socket.gaierror as error: # throwing exception
            print("Error of connecting to FTP", error)

    # for socket programming scenario
    if (option.lower() == 'socket'):
        print("Choose: TCP or UDP")
        type_of_connection = input()
        if (type_of_connection.lower() == 'tcp'):
            print("Working with TCP: ")
            client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_tcp.connect(('localhost', 12345))
            message = input("Write a message: ")
            send_msg_tcp(message)
        if(type_of_connection.lower() == 'udp'):
            print("working with UDP: ")
            message = input("Write a message: ")
            client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_udp.connect(('localhost', 12346))
            server_udp_thread = threading.Thread(target=server_udp_start, daemon=True)
            server_udp_thread.start()
            send_msg_udp(message)
        else:
            print("Your choice is empty!")
