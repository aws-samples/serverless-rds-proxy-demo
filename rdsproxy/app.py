import json
import boto3
from os import environ

import psycopg2

localstackHost = f"http://{environ.get('LOCALSTACK_HOSTNAME')}:{environ.get('EDGE_PORT')}"
client = boto3.client('rds', endpoint_url=localstackHost)  # get the rds object


def create_proxy_connection_token(username):
    # get the required parameters to create a token
    region = environ.get('region')  # get the region
    hostname = environ.get('LOCALSTACK_HOSTNAME')  # get the rds proxy endpoint
    port = 4510 # get the database port

    # generate the authentication token -- temporary password
    token = client.generate_db_auth_token(
        DBHostname=hostname,
        Port=port,
        DBUsername=username,
        Region=region
    )

    return token


def db_ops():
    username = "test_iam_user"

    token = create_proxy_connection_token(username)

    try:
        # create a connection object
        connection = psycopg2.connect(
            host=environ.get('LOCALSTACK_HOSTNAME'),
            database=environ.get('database'),
            user=username,
            password=token,
            port= 4510,
        )

    except psycopg2.Error as e:
        print(e)
        return e

    return connection


def lambda_handler(event, context):
    conn = db_ops()
    print("connection rds proxy : ", conn)
    cursor = conn.cursor()
    query = "SELECT version()"
    cursor.execute(query)
    results = cursor.fetchmany(1)

    return {
        'statusCode': 200,
        'body': json.dumps(results, default=str)
    }
