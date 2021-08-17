import json
import boto3
from os import environ
from aws_lambda_powertools.utilities import parameters

import pymysql


client = boto3.client('rds')  # get the rds object


def db_ops():
    secret = parameters.get_secret(environ.get('secret_arn'), transform='json')
    username = secret.get('username')
    password = secret.get('password')

    try:
        # create a connection object
        connection = pymysql.connect(
            host=environ.get('rds_endpoint'),
            # getting the rds proxy endpoint from the environment variables
            user=username,
            password=password,
            db=environ.get('database'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            ssl={"use": True}
        )
    except pymysql.MySQLError as e:
        return e

    return connection


def lambda_handler(event, context):
    conn = db_ops()
    cursor = conn.cursor()
    query = "select curdate() from dual"
    cursor.execute(query)
    results = cursor.fetchmany(1)

    return {
        'statusCode': 200,
        'body': json.dumps(results, default=str)
    }
