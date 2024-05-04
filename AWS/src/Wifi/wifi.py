# Standard Imports
from dotenv import load_dotenv
from os import getenv

# AWS Imports
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


load_dotenv(r"path to environments file if used.")


class WifiError(Exception):
    pass


class WifiPagesFormat():


    def __init__(self):
        self.secret_name = getenv('DB_NAME') # Database name
        self.region_name = getenv('REGION1') # Database region
        self.id, self.key = self._get_auth() # pyright: ignore

        self.db = boto3.resource('dynamodb', self.region_name)
        self.client = boto3.client('dynamodb', self.region_name)
        self.table_name = "Wifi"
    

    def _get_auth(self):
        key = ""
        value = ""
        

        # Create a Secrets Manager client
        session = boto3.session.Session() # pyright: ignore
        client = session.client(
            service_name='secretsmanager',
            region_name=self.region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.secret_name
            )
        except ClientError as err:
            raise WifiError({
                'Message': 'Error retrieving credentials for DB',
                'exception': str(err)
            })

        secret = get_secret_value_response['SecretString']
        secret = eval(secret)
        try:
            for key, value in secret.items():
                return key, value
        except Exception as err:
            raise WifiError({
                'Message': 'Error retrieving credentials for DB',
                'exception': str(err)
            })


    def _get_table(self):
        table = self.db.Table(self.table_name)
        response = table.scan()
        items = response["Items"]
        for item in items:
            # DynamoDB requires that floats be stored as "Decimal".
            # Convert back to float to be used by required entity.
            item["Price"] = float(item["Price"])
            item["Version"] = int(item["Version"])
            item["Rating"] = float(item["Rating"])

        returnData = self._file_handle(items)

        return returnData


    def _file_handle(self, data):
        wifiData = []
        for item in data:
            if "\\n" in str(item["Description"]):
                data = self._format_list(str(item["Description"]))
                item["Description"] = data
            wifiData.append(item)

        return wifiData
    

    def _format_list(self, desc):
        lines = desc.split("\\n")
        formatted = ""
        for line in lines:
            formatted = formatted + "<li>" + line.strip("\\") + "</li>"
        return(formatted)