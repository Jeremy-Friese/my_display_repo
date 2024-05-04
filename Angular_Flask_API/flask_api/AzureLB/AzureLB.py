# Flask imports
from flask_restful import Resource
from flask import request

# Standard Imports
from datetime import datetime
import json

# API Imports
from AzureLB.AzureLBBuilder import AZBuilder, AZConnectionError

class postAZBuild(Resource): 
    # More functions are available when not the Demo Repo.
    # Dynamic discovery of backend LB, frontend IP config, public IP configs, Sku,
    # and associated VMs.
    def post(body): # type: ignore
        try:
            inputs = request.get_json()
            AZ = AZBuilder(inputs)
            build = AZ.buildLB()
            rule = AZ.addRule()
            val = AZ.validateBuild()
            if val != "Succeeded":
                AZ.deleteLB()
                return {
                    "code": 400,
                    "Message": "Error building ALB",
                    "Response": str(val)
                }
            return {
                "code": 200,
                "Message": "Successfully posted ALB.",
                "Resposne": str(val)
            }
        except AZConnectionError as err:
            if err.args[0]["code"] == 400:
                return {
                    "code": 400,
                    "Message": "Error building ALB",
                    "Response": str(err)
                }