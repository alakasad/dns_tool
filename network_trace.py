# TASK 3: Traceroute and Tracepath
import subprocess
from time import sleep

while True:
    print("Choose: traceroute OR tracepath")

    option = input()
    if(option.lower() == 'traceroute'):
        # getting input from user
        address = input("Please, enter IP address or Domain Name: ")
        if not address:
            print("Input is empty!") # checking for empty string
        else:
            print("Traceroute is executing...")
            # timeout to raise exceptions if exeeds
            result = subprocess.run(["traceroute", address], capture_output=True, text=True, timeout = 100) # subprocess runs traceroute command with given input domain name
            print(result.stdout)
            sleep(2)
    if(option.lower() == 'tracepath'):
        # getting input from user
        address = input("Please, enter IP address or Domain Name: ")
        if not address:
            print("Input is empty!")
        else:
            print("Tracepath is executing...")
            result = subprocess.run(["tracepath", address], capture_output=True, text=True, timeout = 100) # arguments capture_output and text is True to print all information
            print(result.stdout)
            sleep(2)
