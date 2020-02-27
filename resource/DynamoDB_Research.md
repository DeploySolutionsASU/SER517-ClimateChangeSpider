**DynamoDB**
**Introduction**
    1) DynamoDB is the key-value/document fully manages NoSQL database.
    2) DynamoDB global tables replicate the data across multiple AWS Regions to give fast, 
    local access to data for globally distributed applications.
    3) It automatically scales up and down to maintain performance and adjust the volume of data.
    4) A row is called as Item and Column is called as an attribute
    5) DynamoDB supports nested attributes up to 32 levels deep.
    
**Read Capacity** 4kb per second
    1. One strongly consistent read per second
    2. Two eventually consistent read per second (Not consistent) (Default)
    1 read in strongly consistent is equal to 2 reads in eventually consistent
        Disadvantages of strongly consistent 
            •	May not be available during network delay or outage
            •	Higher latency 
            •	Not supported for global secondary indexes
            
**Write Capacity** 1kb per second

**Create table in DynamoDB**
    1) Go to AWS console
    2) Search for DynamoDB and click create a table
    3) Provide table name and primary key, use default settings and click create button
    
**Insert data in DynamoDB**
    1) Click the items tab and click create item to insert data into the table 
    2) Data can be inserted programmatically using Lambda function
    3) Data will be displayed in Tree and also JSON format
    
**Create IAM roles to access the DynamoDB by lambda function**
    I have created table name as "Files"
    ARN under overview is the unique id “Example: arn:aws:dynamodb:us-east-1:070255336900:table/Files”
    
--> To create roles for DynamoDB and Lambda:
    1) Go to IAM and click on roles in the left
    2) Click on lambda if we want to access our DynamoDB from lambda and click next
    3) Add AWSLambdaBasicExecution role and create it
    4) Add one more role by clicking AWSLambdaBasicExecution (Add inline role)
        - Click add actions and add getItem and putItem
    5) Under Resource’, click add ARN and add the ARN name of our table
    6) Give some name for the role (Eg: LambdaDynamoDBRole) 
    7) We can assign this role to our lambda so that they can access the dynamoDB
    
**Create Lambda function**
    1) Search for lambda in the services and click create a function
    2) Provide name and select runtime for the lambda and use an existing role 
    (Eg: LambdaDynamoDBRole) to choose the one we created previously to access DynamoDb, 
    then click create function.

--> Create S3 bucket

--> Add policies to the lambda (Eg: LambdaDynamoDBRole) to access S3
    1) CloudWatchFullAccess
    2) AmazonS3ReadOnlyAccess
    
--> Go to Lambda and add trigger, select S3 and name of the bucket, 
    1) I have added object creation as a trigger
    2) In the configuration we can configure when to trigger our lambda like object 
    creation (Uploading a file), deleting a file etc.
    
Now, once we upload a file in S3 the lambda will get triggered.In lambda, we can use the Boto3 python package
to access the DynamoDB table to insert the data coming from S3.

**References**
    • https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
    • https://www.youtube.com/watch?v=ijyeE-pXFk0&t=1335s
