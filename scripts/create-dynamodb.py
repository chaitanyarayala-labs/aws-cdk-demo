'''
Create a dyanamoDB table called Movies in isolation with aws-cdk.
Link to this table later in a lambda function for CRUD operations.
To run this script:
1. Spin local dynamoDB using docker by running - "docker run -p 8080:8000 amazon/dynamodb-local".
2. Get into virtual env by running - "pipenv shell"
3. Install "aws-cli" and "boto3" by running - "pipenv install"
4. Execute this script by running - "python3 create-dynamodb.py" from scripts directory.
5. If table already exist, it would fail else check table by running - "aws dynamodb list-tables --endpoint-url=http://localhost:8000"
'''
import boto3
import logging
from botocore.exceptions import ClientError
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_local = input('Do you want to create tables locally?(Y/N)\nY: localhost:8000\nN: DynamoDB in the cloud): ')
profile = input('Please input the valid AWS profile you want to use: ')
dynamoDB = None
if is_local in 'nN':
    dynamoDB = boto3.Session(profile_name=profile).resource('dynamodb')
else:
    dynamoDB = boto3.Session(profile_name=profile).resource('dynamodb', endpoint_url='http://localhost:8000/')

movies_table = 'Movies'
logger.info("Starting to create table: {table_name}".format(table_name=movies_table))

try:
    table = dynamoDB.create_table(
        TableName = movies_table,
        KeySchema = [
            {
                'AttributeName': 'year',
                'KeyType': 'HASH' #Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE' #Sort key
            }
        ],
        AttributeDefinitions = [
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput = {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    logger.info("Table status: {status}".format(status=table.table_status))

    if ('ACTIVE' != table.table_status):
        table.meta.client.get_waiter('table_exists').wait(TableName=movies_table)

    logger.info("talbe: {table_name} was successfully created.".format(table_name=movies_table))
except ClientError as e:
    if 'ResourceInUseException' == e.response['Error']['Code']:
        logger.error('table: {name} already exists, can\'t create it again'.format(name=status_table))
    else:
        traceback.print_exc()