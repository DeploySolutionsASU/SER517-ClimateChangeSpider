**Apache Tomcat Installation in AWS EC2 instance**

***Steps***

1. Install Java in the instance if already not installed, 
using \
***sudo yum install java-1.8.0***

2. Install Tomcat using the command, \
***sudo yum install tomcat8 tomcat8-webapps tomcat8-admin-webapps tomcat8-docs-webapp***

3. Start the Tomcat service using the command, \
***service tomcat8 start***

4. Check the installation of Tomcat in the EC2 instance using the  following commands:, 

    1. ***fuser -v -n tcp 8080***, \
    to display the process id (PID) of every process using the specified files.

    2.  ***netstat -na | grep 8080***, \
    to list out all the network (socket) connections on the system.

Apache Tomcat server can be accessed by using the Public IP address of the EC2 instance and the port number (8080).

For example : Open a browser and go to say, 4.12.29.33:8080 to access apache tomcat running on AWS EC2 instance.


