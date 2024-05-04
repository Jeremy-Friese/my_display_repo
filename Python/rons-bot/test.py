#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import os
import sys
import random
import cv2

filepath = "ht"
coin = os.listdir(filepath)
pic = random.choice(coin)
if "ds" in pic.lower():
    print("Done")
    pic = random.choice(coin)
print(filepath + "/" + pic)