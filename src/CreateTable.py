import boto3
from Logger import log_message

dynamodb = boto3.client('dynamodb')

try:
    primaryTable = dynamodb.create_table(
        TableName='primaryTable',
        KeySchema=[
            {
                'AttributeName': 'job_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'job_id',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    log_message("Primary table created")
    

except dynamodb.exceptions.ResourceInUseException:
    log_message("Primary table already exists")

try:
    secondaryTable = dynamodb.create_table(
        TableName='secondaryTable',
        KeySchema=[
            {
                'AttributeName': 'partition_id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'partition_id',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    log_message("Secondary table created")

except dynamodb.exceptions.ResourceInUseException:
    log_message("Secondary table already exists")


