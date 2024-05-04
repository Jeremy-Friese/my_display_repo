# Flask imports
from flask_restful import Resource
from flask import request

# Standard Imports
from datetime import datetime
import json

# API Imports
from AS3.F5AS3 import AS3Compare, ConnectionException


class getDelcaration(Resource):

    def post(body):
        inputs = request.get_json()
        as3 = AS3Compare(inputs)
        try:
            returnFile = as3._connect()
            return returnFile
        except ConnectionException as e:
            return {
                "code": 500,
                "errorCode": e.args[0]["code"],
                "message": e.args[0]["response"],
            }
        