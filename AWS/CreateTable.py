import boto3

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

    print("Job table created")
    

except dynamodb.exceptions.ResourceInUseException:
    print("Job table already exists")

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

    print("Partition table created")

except dynamodb.exceptions.ResourceInUseException:
    print("Partition table already exists")
