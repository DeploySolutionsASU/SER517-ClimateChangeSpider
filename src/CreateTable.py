import boto3
from Logger import log_message

dynamodb = boto3.client('dynamodb')

try:
    jobTable = dynamodb.create_table(
        TableName='jobTable',
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

    log_message("Job table created")
    

except dynamodb.exceptions.ResourceInUseException:
    log_message("Job table already exists")

try:
    partitionTable = dynamodb.create_table(
        TableName='partitionTable',
        KeySchema=[
            {
                'AttributeName': 'partition_id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'job_id',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'partition_id',
                'AttributeType': 'N'
            },
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

    log_message("Partition table created")

except dynamodb.exceptions.ResourceInUseException:
    log_message("Partition table already exists")
