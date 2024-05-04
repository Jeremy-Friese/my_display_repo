# Standard Imports
from dotenv import load_dotenv
from os import getenv
import base64
from datetime import datetime
import json
import time
import traceback
import logging

# Flask
from flask_restful import Resource
from flask import request
from flask import send_from_directory

# Imports used for testing.  Delete before moving to Prod.
import os
import requests

# Custom Imports


class ConnectionException(Exception):
    pass

class AS3Compare(Resource):
    # Possible Unbound errors are ignored with '# type: ignore'
    def __init__(self, inputs):
        self._base64_f5 = self._get_auth()
        self._instance_key = datetime.now().strftime("%m/%d/%y %H:%M:%S")
        self.devices = inputs
        # Will only log locally.  SPLUNK and other report logging is from custom imports.
        logging.basicConfig(filename="./logs.txt", level=logging.DEBUG)
        self._logger = logging.getLogger()
    

    def _get_auth(self):
        '''Retrieves the pan_auto credentials from Thycotic'''
        # load environment variables.
        # Auth to F5 devices goes here.
        # Create temp Username, Password
        f5_username = "Username"
        f5_secret = "Password"
        cred = f"{f5_username}:{f5_secret}"
        cred_bytes = bytes(cred, 'utf-8')
        cred_64 = base64.b64encode(cred_bytes)
        cred_64_final = cred_64.decode()

        return cred_64_final
    

    def _retry(self, headers, taskID):
        counter = 0
        counter500 = 0
        while True:
            url = f"https://{self.devices['device']}/mgmt/shared/appsvcs/task/{taskID}"
            try:
                resp = requests.get(url, headers=headers, verify=False)
                resp.raise_for_status()
            except requests.exceptions.RequestException as e:
                if resp.status_code == 500: # type: ignore
                    time.sleep(10)
                    counter500 += 1
                    if counter500 >= 3:
                        self._logger.critical({
                        "exception": str(e),
                        "message": f"Exception occured retrieving LTM Declaration on {self.devices['device']}.  500 error encounter 3 times while checking process ID",
                        })
                        raise ConnectionException({"code": resp.status_code, # type: ignore
                            "response": f"Exception occured retrieving LTM Declaration on {self.devices['device']}. 500 error encounter 3 times while checking process ID"})
                    else:
                        continue
                else:
                    self._logger.critical({
                    "exception": str(e),
                    "message": f"Exception occured retrieving LTM Declaration on {self.devices['device']}.",
                    })
                    raise ConnectionException({"code": resp.status_code,# type: ignore
                        "response": f"Exception occured retrieving LTM Declaration on {self.devices['device']}."})
            data = json.loads(resp.text)
            returnCode = "Error retrieving code.  Check Logs for details."
            try:
                message = data["results"][0]["message"]
                returnCode  = data["results"][0]["code"]
            except KeyError:
                raise ConnectionException({"code": returnCode,
                                "response": data["message"]})

            if message == "in progress":
                time.sleep(3)
                counter += 1
                if counter == 5:
                    self._logger.critical({
                        "exception": 500,
                        "response": f"Checked results {str(counter)} times with no successful return.  {message}",
                        "code": 1
                    })
                    raise ConnectionException({"code": returnCode,
                                "response": message})
                else:
                    continue
            elif returnCode != 200:
                self._logger.critical({
                    "exception": returnCode,
                    "response": message,
                })
                raise ConnectionException({"code": returnCode,
                            "response": message})
            else:
                return data
                

    def _connect(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self._base64_f5}"
        }

        self.devices["data"]["declaration"]["controls"] = {
        "class": "Controls",
        "trace": True,
        "traceResponse": True,
        "logLevel": "debug",
        "dryRun": True
        }
        
        payload = self.devices["data"]
        try:
            url = f"https://{self.devices['device']}/mgmt/shared/appsvcs/declare?async=true"

            resp = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
            resp.raise_for_status()
            data2 = json.loads(resp.text)
            taskID = data2["id"]
            data = self._retry(headers, taskID)
        except requests.exceptions.RequestException as e:
            if resp.status_code == 500:# type: ignore
                self._logger.critical({
                    "exception": str(e),
                    "message": f"Exception occured retrieving LTM Declaration on {self.devices['device']}.  On initial declaration with error {str(resp.status_code)}", # type: ignore
                    "traceback": traceback.format_exc()
                })
                raise ConnectionException({"code": resp.status_code, # type: ignore
                            "response": f"Exception occured retrieving LTM Declaration on {self.devices['device']} on initial declaration."})
            else:
                self._logger.critical({
                    "exception": str(e),
                    "message": f"Exception occured retrieving LTM Declaration on {self.devices['device']}.  On initial declaration with error {str(resp.status_code)}", # type: ignore
                    "traceback": traceback.format_exc()
                })
                raise ConnectionException({"code": resp.status_code, # type: ignore
                            "response": f"Exception occured retrieving LTM Declaration on {self.devices['device']} with error 'f{str(e)}'"})
   
        tenant = data["results"][0]["tenant"]
        returnJson = {}
        returnJson["tenant"] = tenant
        tempJson = {}
        tempList = []
        
        try:
            for item in data["results"][0]["changes"]:
                detailsItem = ""
                fromItem = None
                toItem = None
                nItem = item["kind"]
                iDetails = item["path"]
                detailsItem = str(item["path"]).replace(",", " | ").strip("[").strip("]")
                if str(item["kind"] ).lower() == "n":
                    nItem = "New"
                    fromItem = item["lhsCommand"]
                    toItem = item["rhsCommand"]
                elif str(item["kind"]).lower() == "d":
                    nItem = "Deleted"
                    fromItem = item["lhsCommand"]
                    toItem = item["rhsCommand"]
                elif str(item["kind"]).lower() == "e":
                    nItem = "Edited"
                    try:
                        fromItem = item["lhs"]
                        toItem = item["rhs"]
                    except KeyError:
                        fromItem = item["lhsCommand"]
                        toItem = item["rhsCommand"]
                if fromItem != None and toItem != None:
                    tempJson = {
                            "Change": nItem,
                            # "Object": item["commad"],
                            "From": fromItem,
                            "To": toItem,
                            "Details": detailsItem
                    }
                elif fromItem == None and toItem != None:
                    self._logger.critical({
                            "message": "Failed to parse F5 response, possible malformed json.",
                            "tenant": tenant
                        })
                elif fromItem != None and toItem == None:
                    self._logger.critical({
                            "message": "Failed to parse F5 response, possible malformed json.",
                            "tenant": tenant
                        })
                tempList.append(tempJson)
        except KeyError as e:
            self._logger.critical({
                "exception": str(e),
                "message": "Failed to parse F5 response, possible malformed json.",
                "tenant": tenant
            })
            raise ConnectionException({
                "F5Response": str(e),  "code": 300,
                "response": "Failed to parse F5 response, possible malformed json."
            })

        returnJson[tenant] = tempList
        self._logger.info({
            "message": f"Sucessfully pulled declaration for {tenant} on on {self.devices['device']}."
        })
        return [json.dumps(data), json.dumps(returnJson)]
        
 