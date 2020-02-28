***************************StartUp Script***************************

To run our application on EC2 instances we have to provide to EC2  as startup script
Startup script can be provided to EC2 instances in two different ways:
****While launching the instance****
    This can be done by providing the script file as part of the USER DATA on the AWS console.
    Or directly run a command that executes our program on the launch of the instance
    
****By modifying the ssh file in /etc.init.d****
    In this case we have to go to the start method of this script and provide a command to start
     our application (python MainScraper.py)

Advantage of going by second way is the script starts on every reboot of the instance. In the first
case script is invoked only at the first startup of the instance.
     

