import boto3

dynamodb = boto3.resource('dynamodb')

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

primaryTable.meta.client.get_waiter('table_exists').wait(TableName='primaryTable')

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

secondaryTable.meta.client.get_waiter('table_exists').wait(TableName='secondaryTable')


