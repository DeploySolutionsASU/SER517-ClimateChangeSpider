**Handling end trigger when an instance gets deallocated**

Spot instance can be terminated by Amazon EC2 with two minutes of notification
The Spot Instance interruption notice also became available as an event in Amazon CloudWatch Events.
This allows targets such as AWS Lambda functions or Amazon SNS topics to process Spot Instance interruption 
notices by creating a CloudWatch Events rule to monitor for the notice.

Step 1: Create a lambda from services and provide necessary roles to access the cloud watch
Step 2: Go to Cloud watch management console and click Events in the left pane and click get started
Step 3: Under Event source, select service name (EC2) from the dropdown and In event type, select Spot instance 
        interruption warning.
Step 4: Under Target, select the lambda function which we have created already and click Configure details
        There are other options like Matched Event, Part of matched event, constant, Input transformer
        to configure input.
Step 5: On the next page, provide the name for rule definition and description and create the rule.
Step 6: Go to lambda console and we can see the connection between the cloud watch event and lambda
Step 7: Now when the spot instance going to terminate the lambda will get triggered and we can do necessary steps
        before the instance get terminated (like updating the status in the database)

Step 8(optional): We can add the trigger in lambda also by clicking add trigger in the lambda and select
                  CloudWatch Events/EventBridge in the Trigger configuration and add rule in voc-ec2-cw-rule
                  
Example event pattern:
        {
          "source": [
            "aws.ec2"
          ],
          "detail-type": [
            "EC2 Instance State-change Notification"
          ],
          "detail": {
            "state": [
              "running",
              "stopped",
              "terminated"
            ]
          }
        }


**References**
https://aws.amazon.com/blogs/compute/taking-advantage-of-amazon-ec2-spot-instance-interruption-notices/
https://ec2spotworkshops.com/ec2_spot_fleet_web_app/spot_interruption.html
