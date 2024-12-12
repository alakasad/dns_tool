# TASK 5:
# COMBINE dns_tool.py + network_trace.py

# all libraries needed:
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

# function to read command and call it in other type of functions:
def get_command():
    command_ex = entry_dname.get()
    if not command_ex:
        result.config(text = "Sorry, your domain name is empty")
    else:
        result.config(text = "The result of the command is: ")
        return command_ex

# cleaning output function:
def clean():
    result.config(text = "Waiting for domain name...")
    result_http.config(text = "Waiting for server or port input to make HTTP Get request...")
    result_ftp.config(text = "Waiting for server to make and FTP connection...")

# following functions are to execute nslookup, dig or host, all DNS commands
def ns():
    command_ns = get_command()
    result_command = subprocess.run(["nslookup", command_ns], capture_output=True, text=True, check=True) # subprocess executes nslookup and takes argument for its destination as command_ns
    # print(result_command.stdout)
    result.config(text = result_command.stdout) # prints the text of result_command object

def dig():
    command_dig = get_command()
    result_command1 = subprocess.run(["dig", command_dig], capture_output=True, text=True, check=True) # text is True so output is text, and capture_output is True to call text.stdout later
    # print(result_command1.stdout)
    result.config(text = result_command1.stdout)

def host():
    command_host = get_command()
    result_command2 = subprocess.run(["host", command_host], capture_output=True, text=True, check=True) #check is True means specific exception CalledProcessError will be called, to handle specific errors
    # print(result_command2.stdout)
    result.config(text = result_command2.stdout)

def get_http():
    http = "http://"
    separator = ":"
    server = entry_http_server.get()
    port = entry_http_port.get()
    if not server or not port:
        result_http.config(text = "Sorry, either your server or port is empty.")
    else:
        url = f"{http}{server}{separator}{port}" #making url from inputs
        params = None # no other parameters will be considered
        request = requests.get(url, params = params)
        result_http.config(text = request.text)
        # print(request.text) # for testing

def connect():
    user = "demo"
    password = "password" # for test.rebex.net it is default values for user and password
    host_name = entry_ftp.get()
    try:
        # print("Connecting to the FTP server...")
        ftp_obj = FTP() # creating FTP object
        with ftp_obj as ftp: # to properly work with FTP object protocol
            ftp.connect(host_name, port=21) # connecting to server
            ftp.login(user = user, passwd = password) # login to server
            # print("Successful connection!")
            result_ftp.config(text = "Successful connection!")
        # print("Closing the connection...")
        # result_ftp.config(text = "Closing the connection...")
    except socket.gaierror as error: # this type of error was common so i needed to catch it
        # print("Error of connecting to FTP", error)
        result_ftp.config(text = "Some error appeared")

# functions to execute traceroute and tracepath
def traceroute():
    status.config(text = "Traceroute is executing. Please, wait...")
    sleep(2) # so that status text would be displayed before the execution of traceroute
    address_route = entry_network_trace.get() # getting value from entry
    if not address_route:
        result_network.config(text = "Sorry, your IP address or Domain Name is empty.")
    else:
        result = subprocess.run(["traceroute", address_route], capture_output=True, text=True, check=True)
        result_network.config(text = result.stdout)

def tracepath():
    status.config(text = "Tracepath is executing. Please, wait...")
    sleep(2)
    address_route = entry_network_trace.get()
    if not address_route:
        result_network.config(text = "Sorry, your IP address or Domain Name is empty.")
    else:
        result = subprocess.run(["tracepath", address_route], capture_output=True, text=True, check=True)
        result_network.config(text = result.stdout)

# cleaning the output function for network tracing block
def clean_network():
    status.config(text="Status of execution")
    result_network.config(text = "Waiting for IP Address or Domain Name...")

# tcp connection sendind function
def send_msg_tcp():
    message_from_client = entry_tcp.get()
    client_tcp.send(message_from_client.encode('utf-8')) # send method of tcp to send message from client

# function to work with client
def handle_client(client):
    while True:
        message = client.recv(4096)
        if not message:
            print("Message is empty!")
            break
        decoded_message = message.decode('utf-8') # decoding message received from client
        # print("Server: received some message from client")
        # print(decoded_message)
        result_server.config(text = "Echo message from server is: " + decoded_message)
        # echo the message
        client.send(message) # Echoing message back to client to check functionality

    client.close() # closing connection out of loop

# establishing tcp server:
def server():
    ip_address = 'localhost'
    port = 12345
    server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_tcp.bind((ip_address, port))
    server_tcp.listen() # listening to client

    while True:
        client, address = server_tcp.accept()
        print("Accepted connection")
        client_thread = threading.Thread( # handling each client by make threads
                    target=handle_client,
                    args=(client,)
        )
        client_thread.start()

# function to start UDP server:
def server_udp_start():
    while True:
        message, address = server_udp.recvfrom(4096) # in UDP server, recvfrom() method is used
        print("Server: message from client: ")
        print(message.decode('utf-8')) # decoding message from client
        result_udp.config(text = "Server received:  " +  message.decode('utf-8')) #printing the message received
    server_udp.close()

def send_msg_udp():
    address = ('localhost', 12346)
    message_from_client = entry_udp.get()
    client_udp.sendto(message_from_client.encode('utf-8'), address) #in UDP, client has sendto() function with additional parameter of address

# initializing the main window of Network Utility Tool
menu = tk.Tk()
menu.title("Network Utility Tool")
menu.geometry("700x600") # initial size of the window

notebook = ttk.Notebook(menu) #using ttk module to create tabs for DNS Commands, Network Tracing and Socket Programming

# DNS Tools:
frame_dns = ttk.Frame(notebook)
notebook.add(frame_dns, text = "DNS")
label= tk.Label(frame_dns, background = "orange", text = "This is DNS Tool").pack(fill = tk.BOTH)
label2 = tk.Label(frame_dns, background = "blue", text = "DNS Commands").pack(fill = tk.BOTH)

# DNS Commands:
question = tk.Label(
        frame_dns,
        text="Please, enter domain name: ").pack(expand = True) # arguments in pack() expand is True allows to expand elements when expanding the window

# input domain name
entry_dname = ttk.Entry(frame_dns)
entry_dname.pack(pady = 5, expand = True)

# frame to put all buttons in one place
frame_buttons = ttk.Frame(master=frame_dns)
frame_buttons.pack(expand = True, fill = tk.BOTH)
# buttons to choose the DNS related command to execute
button = tk.Button(frame_buttons, text="nslookup", command=ns).pack(side=tk.LEFT, padx=5, expand = True, fill = tk.BOTH)
button1 = tk.Button(frame_buttons, text="dig", command=dig).pack(side=tk.LEFT, padx=5, expand = True, fill = tk.BOTH)
button2 = tk.Button(frame_buttons, text="host", command=host).pack(side=tk.LEFT, padx=5, expand = True, fill = tk.BOTH)
button3 = tk.Button(frame_buttons, text="Clean output", command=clean).pack(side=tk.LEFT, expand = True, fill = tk.BOTH) # button to clean output

# frame to display result
frame_results = tk.Frame(master=frame_dns).pack(expand = True, fill = tk.BOTH)
result = tk.Label(frame_dns, text="Waiting for domain name...")
result.pack(expand = True, fill = tk.BOTH)

# TASK 2
# frame to work with protocols and put all elements inside of it
frame_protocols = tk.Frame(master=frame_dns).pack(expand = True, fill = tk.BOTH)
description = tk.Label(
        frame_dns,
        background = "orange",
        text="Making HTTP and FTP requests:").pack(fill = tk.BOTH)

description = tk.Label(
        frame_dns,
        text="HTTP",
        background = "blue"
        ).pack(expand = True, fill = tk.BOTH)

question = tk.Label(
        frame_dns,
        text="Target server:").pack(expand = True, fill = tk.BOTH)
# input domain name
entry_http_server = tk.Entry(frame_dns)
entry_http_server.pack(pady = 10, expand = True, fill = tk.BOTH)

question = tk.Label(
        frame_dns,
        text="Target port:").pack(expand = True, fill = tk.BOTH)
# input target port
entry_http_port= tk.Entry(frame_dns)
entry_http_port.pack(pady = 10, expand = True, fill = tk.BOTH)

# frame for buttons of HTTP part:
frame_buttons2 = tk.Frame(master=frame_dns)
frame_buttons2.pack(expand = True, fill = tk.BOTH)
button_http = tk.Button(frame_buttons2, text="GET", command=get_http).pack(side=tk.LEFT, padx=5, expand = True, fill = tk.BOTH) # command is get_http() function declared earlier
button3 = tk.Button(frame_buttons2, text="Clean output", command=clean).pack(side=tk.LEFT, expand = True, fill = tk.BOTH)

# displaying results as a Label:
result_http = tk.Label(frame_dns, text="Waiting for server or port input to make HTTP Get request...")
result_http.pack(expand = True, fill = tk.BOTH)

# working with FTP connection:
description = tk.Label(
        frame_dns,
        text="FTP",
        background = "blue"
        ).pack(expand = True, fill = tk.BOTH)

question = tk.Label(
        frame_dns,
        text="Host for FTP:").pack(expand = True, fill = tk.BOTH)
# getting input of host name from FTP
entry_ftp = tk.Entry(frame_dns)
entry_ftp.pack(pady = 10, expand = True, fill = tk.BOTH)

# buttons to establish Connection
frame_buttons3 = tk.Frame(master=frame_dns)
frame_buttons3.pack(expand = True, fill = tk.BOTH)
button_ftp = tk.Button(frame_buttons3, text="Connect", command=connect).pack(side=tk.LEFT, padx=5, expand = True, fill = tk.BOTH)
button4 = tk.Button(frame_buttons3, text="Clean output", command=clean).pack(side=tk.LEFT, expand = True, fill = tk.BOTH)

result_ftp = tk.Label(frame_dns, text="Waiting for server to make and FTP connection...")
result_ftp.pack(expand = True, fill = tk.BOTH)

# NETWORK TRACING:
frame_tracing = ttk.Frame(notebook)
notebook.add(frame_tracing, text = "N.T.")
label= tk.Label(frame_tracing, background = "orange", text = "Network Tracing").pack(expand = True, fill = tk.BOTH)
question = tk.Label(
        frame_tracing,
        text="Please, enter IP address or Domain Name: ").pack()
entry_network_trace = ttk.Entry(frame_tracing)
entry_network_trace.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)
frame_buttons_network = tk.Frame(master=frame_tracing)
frame_buttons_network.pack(expand = True, fill = tk.BOTH)
button_route = tk.Button(frame_buttons_network, text="traceroute", command=traceroute).pack(padx=5, pady=5, expand = True, fill = tk.BOTH)
button_path = tk.Button(frame_buttons_network, text="tracepath", command=tracepath).pack(padx=5, pady=5, expand = True, fill = tk.BOTH)
button_clean = tk.Button(frame_buttons_network, text="Clean output", command=clean_network).pack(padx=5, pady=5, expand = True, fill = tk.BOTH)

# displaying status of commands as they are executed as 30 iterations
status = tk.Label(frame_tracing, text = "Status of execution")
status.pack(expand = True, fill = tk.BOTH)

result_network = tk.Label(frame_tracing, text = "Waiting for IP Address or Domain Name...")
result_network.pack(expand = True, fill = tk.BOTH)

# SOCKET PROGRAMMING:
frame_socket = ttk.Frame(notebook)
notebook.add(frame_socket, text = "S.P.")
label= tk.Label(frame_socket, background = "orange", text = "Socket Programming").pack(expand = True, fill = tk.BOTH)

# TCP Connection:
# thread for server, because client and server are running in one python file:
server_thread = threading.Thread(target=server)
server_thread.start()

frame_servers = ttk.Frame(master=frame_socket)
frame_servers.pack(expand = True, fill = tk.BOTH)

# separating frames for TCP and UDP connections to place them as Columns
frame_tcp = ttk.Frame(frame_servers, borderwidth=1, relief="solid")
frame_udp = ttk.Frame(frame_servers, borderwidth=1, relief="solid")
# placing them in columns, by side argument
frame_tcp.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame_udp.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
label_tcp = ttk.Label(frame_tcp, text="TCP", background = "blue")
label_tcp.pack(expand = True, fill = tk.BOTH)
label_udp = ttk.Label(frame_udp, text="UDP", background = "blue")
label_udp.pack(expand = True, fill = tk.BOTH)

listening_msg = tk.Label(frame_tcp, text="Listening on localhost and on 12345 port...")
listening_msg.pack(expand = True, fill = tk.BOTH)

question = tk.Label(
        frame_tcp,
        text="Please, write message:").pack(expand = True, fill = tk.BOTH)
# input of message from client
entry_tcp = ttk.Entry(frame_tcp)
entry_tcp.pack(pady = 5)

button_tcp = ttk.Button(frame_tcp, text = "Send message", command=send_msg_tcp)
button_tcp.pack()

result_server = tk.Label(frame_tcp, text="Waiting response from the server...")
result_server.pack(expand = True, fill = tk.BOTH)

# creating new client for TCP connection
client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_tcp.connect(('localhost', 12345))

# UDP connection:
server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_udp.bind(('localhost', 12346)) # using other port

server_udp_thread = threading.Thread(target=server_udp_start, daemon=True)
server_udp_thread.start() # thread for UDP server, as it also runned with TCP server

listening_msg = tk.Label(frame_udp, text="Connecting on localhost and on 12346 port...")
listening_msg.pack(expand = True, fill = tk.BOTH)

question = tk.Label(
        frame_udp,
        text="Please, write message:").pack(expand = True, fill = tk.BOTH)

# input message from client
entry_udp = ttk.Entry(frame_udp)
entry_udp.pack(pady = 5)

# initializing UDP client
client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_udp.connect(('localhost', 12346))

button_tcp = ttk.Button(frame_udp, text = "Send message", command=send_msg_udp)
button_tcp.pack()

result_udp = tk.Label(frame_udp, text="Result of the server connection will be displayed here")
result_udp.pack(expand = True, fill = tk.BOTH)

notebook.pack(expand = 1, fill = "both")

menu.mainloop() # starts Tkinter
