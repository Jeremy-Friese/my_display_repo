#!/usr/bin/python3

import os
import sys
import time
import ipaddress
import socket
import fcntl
import struct
import sys
import netifaces

def hue_finder(i):
    try:
        finder = socket.gethostbyaddr(str(i))
        if "hue" in finder[0]:
            hue = i
            print(hue)
    except socket.herror:
        pass

def get_network():
    IP1 = socket.gethostbyname(socket.gethostname())
    
    for i in netifaces.interfaces():
        if "lo" not in i:
           iface = i
    net = netifaces.ifaddresses(iface)[2][0]["netmask"]
    if net == "255.255.255.252":
        Mask = "/30"
    if net == "255.255.255.248":
        Mask = "/29"
    if net == "255.255.255.240":
        Mask = "/28"
    if net == "255.255.255.224":
        Mask = "/27"
    if net == "255.255.255.192":
        Mask = "/26"
    if net == "255.255.255.128":
        Mask = "/25"
    if net == "255.255.255.0":
        mask = "/24"

    network = (IP1 + Mask)
    network = list(ipaddress.ip_network(network, False).hosts())
    for i in network:
        hue_finder(i)

if __name__ == "__main__":
    get_network()
