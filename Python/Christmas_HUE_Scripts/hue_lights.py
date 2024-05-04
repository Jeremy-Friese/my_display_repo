#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import os
import sys
import phue
from phue import Bridge
import time
import random
from threading import Thread
import socket
import netifaces
from netifaces import AF_INET
import ipaddress

def light_0(*lights):
    while True:
        rc = random.choice(range(0, 65535 + 1))
        lights[0].on = True
        lights[0].hue = rc
        lights[0].saturation = 254
        lights[0].brightness = 200
        time.sleep(0.75)

def light_1(*lights):
    while True:
        time.sleep(0.375)
        rc = random.choice(range(0, 65535 + 1))
        lights[1].on = True
        lights[1].hue = rc
        lights[1].saturation = 254
        lights[1].brightness = 200
        time.sleep(0.375)
        #lights[1].brightness = 0

def light_6(*lights):
    while True:
        rc = random.choice(range(0, 65535 + 1))
        print(rc)
        lights[6].on = True
        lights[6].hue = rc
        lights[6].saturation = 254
        lights[6].brightness = 200
        time.sleep(2)
        lights[6].brightness = 0
        time.sleep(1)

def light_7(*lights):
    while True:
        rc = random.choice(range(0, 65535 + 1))
        print(rc)
        lights[7].on = True
        lights[7].hue = rc
        lights[7].saturation = 254
        lights[7].brightness = 200
        time.sleep(2)
        lights[7].brightness = 0
        time.sleep(1)

def hue_finder(i):
    try:
        finder = socket.gethostbyaddr(str(i))
        if "hue" in finder[0]:
            global bridge
            bridge = i
            print(bridge)
            return(bridge)
    except socket.herror:
        pass

def get_network():
    for i in netifaces.interfaces():
        print(i)
        """if "lo" not in i:
           iface = i"""
        if i == "en0":
            iface = i
    netInfo = netifaces.ifaddresses(iface)[AF_INET]
    print(netInfo)
    IP1 = netInfo[0]["addr"]
    net = netInfo[0]["netmask"]
    Mask - "24"
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
    #print(network)
    for i in network:
       hue_finder(i)

def get_lights():
    bridge = "192.168.86.33"
    b = Bridge(str(bridge))
    b.connect()
    b.get_api()
    lights = b.lights
    return(lights)


def main():
    newLights = []
    #get_network()
    lights = get_lights()
    for i in lights:
        if "outdoor" in str(i).lower():
            newLights.append(i)
    Thread(target = light_0, args=(lights)).start()
    #time.sleep(0.5)
    Thread(target = light_1, args=(lights)).start()
    #time.sleep(0.5)

if __name__ == "__main__":
    main()
