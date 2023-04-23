import os, json
import urllib3
import boto3
import base64

headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}

success_response = {
    'statusCode': 200,
    'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    },
    'body': json.dumps({
        'success': True
    }),
    "isBase64Encoded": False
}

error_response = {
    'statusCode': 405,
    'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    },
    'body': json.dumps({'error': 'Incorrect request'}),
    "isBase64Encoded": False
}


def get_aws_secrets(env_secrets_name):
    secret_name = os.environ.get(env_secrets_name)
    region_name = os.environ.get('REGION')

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    secret = get_secret_value_response['SecretString']

    return json.loads(secret)