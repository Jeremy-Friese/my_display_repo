# Standard Library imports
from os import getenv
from dotenv import load_dotenv
import base64
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import xmltodict
import json
from netmiko import ConnectHandler, exceptions
from socket import gethostname

import time

# Flask
from flask_restful import Resource

class Testing(Resource):
    def __init__(self, sid, socketio, inputs):
        self.sid = sid
        self.socketio = socketio
        print(inputs)
        time.sleep(4)
    def moreTest(self):
        for i in range(1, 11):
            self.socketio.emit('response', {'data': f'Processing {i*10}%'}, room=self.sid)
            self.socketio.sleep(1)
        return {"message": "This is a data file"}
        # return({"final_message": "This is a data file"})
    