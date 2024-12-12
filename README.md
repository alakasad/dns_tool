This project contains three files named 'dns_tool.py', 'network_trace.py' and 'network_utility.py'.
'network_utility.py' has interface, while other two files executed by commands.

In order to run file, you need:
python version 3.8.10
Tcl/Tk version 8.6
requests version 2.22.0
socket (ftplib too) version corresponds to python version

You need to open 'network_utility.py' to work with network utility tool.
It has three tabs on DNS Commands, Network Tracing and Socket Programming.

DNS Commands contain 'nslookup', 'dig' and 'host' to particular domain name or IP address.
In this tab, you can only make HTTP Get request, or establish connection to FTP server 'test.rebex.net'. (user = 'demo', passwd = 'password')
To connect for other FTP servers, you need to change value of user and password, or port. At this point, port is default 21.

Network tracing works only with 'traceroute example.com' or 'tracepath example.com' commands.
Commands such as 'traceroute -n example.com', 'tracepath -n example.com', 'traceroute -q 3 example.com', 'traceroute -q 3 example.com' are not considered for this version of code.

By choosing the necessary tab, you need to fill input of what is asked.
Otherwise, commands will not be executed, as arguments are empty.
It has buttons to corresponding commands, and clean output button.

In Socket Programming, TCP Server always listens, UDP server just connects.
All messages are encoded and decoded in 'utf-8' only.
