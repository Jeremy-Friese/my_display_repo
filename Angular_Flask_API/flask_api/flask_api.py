# Standard Library imports
from dotenv import load_dotenv
import os

# Flask imports
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_restful import Api
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

# API Imports
from subnetCalc.subnetGetPost import getResults
from AS3 import AS3Declare
from AzureLB import AzureLB


app = Flask(__name__)
# app.json_encoder = LazyJSONEncoder
cors = CORS(app, resources={r"/*": {"origins": "*","allow_headers":"*"}})
api = Api(app)
swagger = Swagger(app)
app.debug = True

SWAGGER_URL = '/swagger-ui'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask API Demo"
    }
)

app.register_blueprint(swaggerui_blueprint)

# API Declarations
api.add_resource(getResults, '/Subnet', '/subnetcalc')
api.add_resource(AS3Declare.getDelcaration, '/AS3', '/AS3Declare')
api.add_resource(AzureLB.postAZBuild, '/AzureLB', '/azure')

if __name__ == "__main__":
    app.run(port=5000, debug=True)