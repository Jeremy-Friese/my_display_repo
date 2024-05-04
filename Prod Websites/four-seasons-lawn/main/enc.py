#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import os
import sys
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import uuid
import socket
import hashlib, binascii
import re
from getpass import getpass
import argparse

class secret(object):
    here = os.getcwd()
    with open(here + "/main/k.out", "rb") as k:
        key = k.read()
    def __init__(self, message):
        self.message = message
    def decrypt(flag):
        here = os.getcwd()
        if flag.lower() == "u":
            with open(here + "/main/f.out", "rb") as data:
                iv = data.read(16)
                ciphered_data = data.read()
        cipher = AES.new(secret.key, AES.MODE_CBC, iv=iv)
        original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size)
        original_data = original_data.decode("utf-8")
        return(str(original_data))

    def encryption(self):
        data = self.message.encode('ascii')
        cipher = AES.new(secret.key, AES.MODE_CBC)
        ciphered_data = cipher.encrypt(pad(data, AES.block_size))
        return(cipher.iv, ciphered_data)


    def updateKey():
        here = os.getcwd()
        data = secret.decrypt("u")
        data = data.encode("ascii")
        tempKey = PBKDF2(secret.pwrd, secret.salt, dkLen=32)
        cipher = AES.new(tempKey, AES.MODE_CBC)
        ciphered_data = cipher.encrypt(pad(data, AES.block_size))
        with open(here + "/main/k.out", "wb") as k:
            k.write(tempKey)
        with open(here + "/main/f.out", "wb") as f:
            f.write(cipher.iv)
            f.write(ciphered_data)
        data2 = secret.decrypt("sp")
        data2 = data2.encode("ascii")
        cipher2 = AES.new(tempKey, AES.MODE_CBC)
        ciphered_data2 = cipher2.encrypt(pad(data2, AES.block_size))
        with open(here + "/sp.out", "wb") as s:
            s.write(cipher2.iv)
            s.write(ciphered_data2)

def get_args(cmdline=None):
    here = os.getcwd()
    newList = []
    parser = argparse.ArgumentParser()
    parser.add_argument(
          "-up",
          "--updateUserPass",
          action="store_true",
          required=False
          )
    parser.add_argument(
          "-k",
          "--keyupdate",
          action="store_true",
          required=False
          )
    parser.add_argument(
          "-p",
          "--printer",
          action="store_true",
          required=False
          )
    args = parser.parse_args()
    message = args.updateUserPass
    keyUpdate = args.keyupdate
    p = args.printer
    if message == True:
        username = input("Username: ")
        password = getpass("Password: ")
        tmpMessage = str(username) + "," + str(password)
        tmpMessage = secret(tmpMessage)
        iv, ciphered_data = tmpMessage.encryption()
        with open(here + "/main/f.out", "wb") as f:
            f.write(iv)
            f.write(ciphered_data)
        if p == True:
            creds = secret.decrypt("u")
            print(creds)
    elif sp == True:
        in1 = input("client_id: ")
        in2 = input("secret_id: ")
        in3 = input("resource_id: ")
        tmpMessage = str(in1) + "," + str(in2) + "," + str(in3)
        tmpMessage = secret(tmpMessage)
        iv, ciphered_data = tmpMessage.encryption()
        with open("sp.out", "wb") as f:
            f.write(iv)
            f.write(ciphered_data)
            f.write(iv)
            f.write(ciphered_data)
        if p == True:
            creds = secret.decrypt("sp")
            print(creds)
    elif keyUpdate == True:
        secret.updateKey()
    else:
        if p == True:
            if sp != True or message != True:
                print("Please update credentials prior to viewing.")

def main():
    get_args()

if __name__ == "__main__":
    main()
