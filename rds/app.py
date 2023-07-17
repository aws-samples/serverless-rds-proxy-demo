import json
import boto3
from os import environ

import psycopg2


localstackHost = f"http://{environ.get('LOCALSTACK_HOSTNAME')}:{environ.get('EDGE_PORT')}"
client = boto3.client('rds', endpoint_url=localstackHost)
sm = boto3.client('secretsmanager', endpoint_url=localstackHost)

def db_ops():
    secret_arn = sm.list_secrets()["SecretList"][0]["ARN"]
    secret = sm.get_secret_value(SecretId=secret_arn)
    username = json.loads(secret["SecretString"]).get('username')
    password = json.loads(secret["SecretString"]).get('password')

    try:
        # create a connection object
        connection = psycopg2.connect(
            host=environ.get('LOCALSTACK_HOSTNAME'),
            database=environ.get('database'),
            user=username,
            password=password,
            port=4510,
        )
    except psycopg2.Error as e:
        print(e)
        return e

    return connection


def lambda_handler(event, context):
    conn = db_ops()
    print("connection: ", conn)
    cursor = conn.cursor()
    query = "SELECT version()"
    cursor.execute(query)
    results = cursor.fetchmany(1)

    return {
        'statusCode': 200,
        'body': json.dumps(results, default=str)
    }
    