#!/usr/bin/python3
import socket
import subprocess
import ipaddress
import sys
import os
import fcntl
#from yes_no import query_yes_no
from ipaddress import *

#This checks for other instances of the sript running.
#pid_file = 'program.pid'
#fp = open(pid_file, 'w')
"""try:
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    print("No other intsances running")
except IOError:
    # another instance is running
    print("Another instance running of this scirpt.  Exiting.")
    sys.exit(0)"""

# Clear the screen
subprocess.call('clear', shell=True)

print("*" * 49)
print("*                                               *")
print("*     YOU ARE ABOUT TO START AN IP SCAN         *")
print("*          THIS CAN ONLY BE DONE ON             *")
print("*           INTERNAL SYSTEMS!                   *")
print("*                                               *")
print("*                                               *")
print("*                                               *")
print("*                                               *")
print("*" * 49)

#Give notification that script will fail on public IP addresses.
print("This scan will only work on private IP addresses")

#query_yes_no("Are you conducting an IP scan on an internal system?")


# Prompt the user to input a network address
net_addr = input("Enter a network address in CIDR format(ex.192.168.1.0/24): ")

# Create the network
ip_net = ipaddress.ip_network(net_addr)

# Get all hosts on that network
all_hosts = list(ip_net.hosts())

if ip_net.is_private is True:

    f = open("ping.txt", "w")
    fw = open("ping_stat.txt", "w")
    try:
        for i in range(len(all_hosts)):
            process = subprocess.Popen(['ping', '-c', '1', '-t', '1', str(all_hosts[i])], stdout=subprocess.PIPE)
            output= process.communicate()[0]
            f.write(output.decode('utf-8'))


            if "ttl=12" in output.decode('utf-8'):
                print(str(all_hosts[i]), "Windows Device is Online")
                fw.write(str(all_hosts[i]) + "Windows Device is Online" + '\n')
            elif "ttl=5" in output.decode('utf-8'):
                print(str(all_hosts[i]), "Linux Device is Online")
                fw.write(str(all_hosts[i]) + "Linux Device is Online" + '\n')
            elif "ttl=6" in output.decode('utf-8'):
                print(str(all_hosts[i]), "Linux Device is Online")
                fw.write(str(all_hosts[i]) + "Linux Device is Online" + '\n')
            elif "ttl=25" in output.decode('utf-8'):
                print(str(all_hosts[i]), "Network Device is Online")
                fw.write(str(all_hosts[i]) + "Network Device is Online" + '\n')
            elif "ttl" in output.decode('utf-8'):
                print(str(all_hosts[i]), "Unkown Device is Online")
                fw.write(str(all_hosts[i]) + "Unkown Device is Online" + '\n')
            elif "0 received" in output.decode('utf-8'):
                print(str(all_hosts[i]), "is Offline")
                fw.write(str(all_hosts[i]) + "offline" + '\n')
            elif "reachable" in output.decode('utf-8'):
                print(str(all_hosts[i]), "is unreachable")
                fw.write(str(all_hosts[i]) + "is unreachable" + '\n')
            else:
                print(str(all_hosts[i]), "is unreachable")
                fw.write(str(all_hosts[i]) + "is unreachable" + '\n')

    except KeyboardInterrupt:
        print ("Scan Ended Manually")
        sys.exit()
    f.close()
    fw.close()

else:
    print("Please use private IP address range")
    sys.exit
