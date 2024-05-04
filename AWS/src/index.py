# Flask imports
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_restful import Api


# AWS Imports
import awsgi

# API Imports
from Wifi.wifi_pages import Wifi

app = Flask(__name__)


CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
}})
api = Api(app)

app.debug = True

# Route Declarations
@app.route('/login', methods=['GET', 'POST'])
def items():
    if request.method == 'POST':
        return 'POST Worked'
    elif request.method == 'GET':
        return 'Get Worked'
    else:
        return 'Incorrect Method'

# API Declarations
api.add_resource(Wifi, '/wifi')

# Configure AWS to handle the API.
def handler(event, context):
    return awsgi.response(app, event, context) #pyright: ignore

# Local Testing
if __name__ == "__main__":
    app.run(port=5000, debug=True)