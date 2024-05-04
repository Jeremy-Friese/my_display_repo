#!/usr/bin/python3
import ipaddress
import socket
import sys
import fcntl
from datetime import datetime
from multiprocessing import Pool
from functools import partial
from errno import *
from yes_no import query_yes_no

#This checks for other instances of the sript running.
"""pid_file = 'program.pid'
fp = open(pid_file, 'w')
try:
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    print("No other intsances running")
except IOError:
    # another instance is running
    print("Another instance running of this scirpt.  Exiting.")
    sys.exit(0)"""

def ping(host, port):
    try:
        socket.socket().connect((host, port))
        print(str(port) + " Open")
        return port
    except socket.error as err:
        if err.errno == ECONNREFUSED:
            return False
        elif err.errno == ETIMEDOUT:
            return False
        raise

def scan_ports(host, x, y):
    p = Pool(100)
    ping_host = partial(ping, host)
    return filter(bool, p.map(ping_host, range(x, y)))


def main():
    print("*" * 49)
    print("*                                               *")
    print("*     YOU ARE ABOUT TO START A PORT SCAN        *")
    print("*          THIS CAN ONLY BE DONE ON             *")
    print("*           INTERNAL SYSTEMS!                   *")
    print("*                                               *")
    print("*                                               *")
    print("*                                               *")
    print("*                                               *")
    print("*" * 49)

    #Give notification that script will fail on public IP addresses.
    print("This scan will only work on private IP addresses")


    # Ask for input
    host = input("Enter a remote host to scan: ")
    min_port = input("Port to Start Scan:")
    max_port = input("Port to End Scan:")
    ip_net = ipaddress.ip_network(host)


    x = int(min_port)
    y = int(max_port)



    # Check what time the scan started
    t1 = datetime.now()

    if ip_net.is_private is True:
        print("\n")
        print("-" * 60)
        print("Please wait, scanning ports on " + host)
        print("-" * 60)
        ports = list(scan_ports(host, x, y))
        print("\nDone.")

        print(str(len(ports)) + " ports available.")
        print(ports)
        # Checking the time again
        t2 = datetime.now()

        # Calculates the difference of time, to see how long it took to run the script
        total =  t2 - t1

        # Printing the information to screen
        print ('Scan Completed in: ', total)
    else:
        print("Please use private IP address range")
        sys.exit


if __name__ == "__main__":
    main()
