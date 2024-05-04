# Flask imports
from flask_restful import Resource
from flask import request

# Standard Imports
from datetime import datetime
import json

# API Imports
from SubnetCalc.subnetHandle import subnetCalc, ConnectionException

class getResults(Resource):

    def post(self):
        try:
            inputs = request.get_json()
            print(inputs)
            results = subnetCalc(inputs)
            returnResults = results._find_smallest_cidr()

            return {
                'statusCode': 200,
                'body': json.dumps(returnResults)
            }
            return(results._find_smallest_cidr())
        except ConnectionException as err:
            print(err.args[0]["code"])
            return {
                "code": err.args[0]["code"],
                "message": err.args[0]["message"]
            }, 400

    def get(self): # type: ignore
        inputs = request.get_json()
        results = subnetCalc(inputs)
        return(results._find_smallest_cidr())