# Flask imports
from flask_restful import Resource
from flask import request

from Wifi.wifi import WifiError, WifiPagesFormat

class Wifi(Resource):
    def get(self):
        try:
            wifi = WifiPagesFormat()
            wifiData = wifi._get_table()
            return wifiData
        except WifiError as err:
            raise WifiError({
                "code": 400,
                "message": "Error occured connecting to database, please check logs",
                "exception": str(err)
            })