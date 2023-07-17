import json
import boto3
from os import environ

import psycopg2


localstackHost = "http://localhost:4566"
client = boto3.client('rds', endpoint_url=localstackHost)
sm = boto3.client('secretsmanager', endpoint_url=localstackHost)

def db_ops():
    secret_arn = sm.list_secrets()["SecretList"][0]["ARN"]
    secret = sm.get_secret_value(SecretId=secret_arn)
    username = json.loads(secret["SecretString"]).get('username')
    password = json.loads(secret["SecretString"]).get('password')

    try:
        connection = psycopg2.connect(
            host="localhost",
            database="mylab",
            user=username,
            password=password,
            port=4510,
        )

    except psycopg2.Error as e:
        return e

    return connection


conn = db_ops()
cursor = conn.cursor()
query = "create user test_iam_user with login"
cursor.execute(query)
conn.commit()
query = "grant rds_iam to test_iam_user"
cursor.execute(query)
conn.commit()

    