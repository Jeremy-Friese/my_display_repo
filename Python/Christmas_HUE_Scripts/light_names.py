#!/usr/bin/python3
  
import os
import sys
import phue
from phue import Bridge
import time

b = Bridge("192.168.37.43")
b.connect()

b.get_api()

lights = b.get_light_objects('id')
light = b.lights
#print(light[0])
#print(light[1])
#print(light[7])
#print(light[6])

for l in light:
    print(l)
