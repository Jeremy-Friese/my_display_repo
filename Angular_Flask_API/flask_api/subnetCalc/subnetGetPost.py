# Flask imports
from flask_restful import Resource
from flask import request

# Standard Imports
from datetime import datetime

# API Imports
from subnetCalc.subnetHandle import subnetCalc, ConnectionException

class getResults(Resource):

    def post(body):
        inputs = request.get_json()
        print(inputs)
        results = subnetCalc(inputs)
        return(results._find_smallest_cidr())
        # fileToReturn = nTest._csvCreate()
        # return(fileToReturn)
    def get(body):
        inputs = request.get_json()
        results = subnetCalc(inputs)
        return(results._find_smallest_cidr())