# Description

**This is meant to be ran in a properly configured Lambda environment with the API Ggateways configured for the proper protocol [OPTIONS, GET, POST, etc.]**


**Pulls data from a DynamoDB Database called 'wifi' and returns it configured to be displayed as html**

**This was designed for and currently running live a version in AWS Amplify**

## Setup

```bash
amplify init
amplity add api
```
*When configuring endpoints name them the same as the API path in the FLask App*

*Your new endpoints must be added to the `packages` list in `setup.py`*

*Any additional modules that are needed for the project have to be added to `Pipfile`.  Think of this as like the `requirements.txt` that come with most projects.

*Add this folder to the `amplify/backend/function{yourLambda}` folder.*

```bash
amplify push -y
```

*  ***Login to the GUI and in the `API Gateway` click on `{yourLambdaFunction}`.***

*  ***Verify that the version of python you specified in the Pipfile is what is being used.***  


**AWS will sometimes revert to Python3.8 and will cause errors if not the same version specified in the Pipfile.**   

## Testing

Alwasy test locally before deploying.  
After pushing to Amplify use the API URL that was given to validate API/s are working as intended.  

```bash
amplify status
```
This command will give you the status of your Lambda function and CloudWatch as well as give the API URL.

***These commands will create additional roles in your AWS environment.***
***If accessing DynamoDB or other resources the role with `{yourLambdaFunction}` in it will need to be given appropriate access!***

# Additional Information

Depending on the setup and the Lambda and API Gateway configuration, each API may need to have additional information returned on each call to prevent the API calls from being blocked by CORS.  The below allows each API endopoint to handle the CORS rather than sitewide in `index.py`.  

```python
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "http://localhost:4200",  # Allows requests from localhost on port 4200
            "Access-Control-Allow-Methods": "POST, OPTIONS",  # Ensures both POST and OPTIONS are supported
            "Access-Control-Allow-Headers": "Content-Type,Authorization"  # Allows Content-Type and Authorization headers
        },
        'body': json.dumps({"message": "Success"})
    }
```