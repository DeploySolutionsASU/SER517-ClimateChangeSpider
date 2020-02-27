***************************** EC2 Instance Setup ******************************

EC2 stands for Elastic Compute Cloud. EC2 instance is a virtual server in the 
AWS. There is another type of EC2 instance called on-demand EC2 instance which
is used by the subscriber/user by renting the virtual server on per hour basis.
This cost also differs based on the type of instance that is chosen. The 
instance can also be chosen based on the requirements of CPU and memory.

The following are the steps that are used to create an instance.
 
STEP - 1 : Login to the AWS account and navigate to the Services tab. All the AWS
           services are categorized based on Compute, Storage, Database etc; In
           order to create the EC2 instance we need to choose EC2 that is under
           compute section.
STEP - 2 : On the top right corner of the dashboard, you need to choose the region
           of the EC2 instance and go back to the EC2 dashboard.
STEP - 3 : Under the Create instance section, click on the Launch Instance button.
STEP - 4 : Now, select the type of AMI (Amazon Machine Image). Once this instance 
           is launched, the AMI instance will be booted with the desired OS.            
STEP - 5 : Choose the type of instance based on the requirements of CPU and memory
           that is needed and click on next.
STEP - 6 : In the next step, enter the number of instances that you would like to 
           setup. If you would like to create spot instances instead of on-demand
           select the checkbox that is under the number of instances section.
STEP - 7 : In the next step, we need to configure the basic networking details like
           the VPC in which you would like to launch, the type of subnet inside the 
           VPC. This need to be well planned. If we are using a web server, public 
           subnet is used and if it is a DB server then private subnet is to be used.
STEP - 8 : IP can be assigned automatically by the AWS. We can also create an IP 
           manually. Mention the IAM role as None.
STEP - 9 : We can define the shutdown behavior. Based on the shutdown behavior we 
           can stop the instance.
STEP - 10: In the next step, storage can be added. By default, a general purpose 
           SSD root volume of 8GB can be provisioned. The volume size and type of
           volume can also be changed.
STEP - 11: The instance can be tagged with a key-value pair which helps in 
           identifying the instance easily.
STEP - 12: The traffic can be restricted by configuring the security group. This is
           the firewall that is provided by AWS apart from your instance's OS firewall.
STEP - 13: Review the setup that is done till this point and launch the instance.
STEP - 14: A key-value pair is to be created so that we can make the instance secure 
           by adding a login feature. AWS provides a private key and that key needs to
           be downloaded and kept safe. This key can't be downloaded again.
STEP - 15: Launch the instance and wait for the instance to be launched.

The setup is complete.

Resource : 
You can refer to the following link if you want much detailed information regarding the
setup process.
LINK : https://www.guru99.com/creating-amazon-ec2-instance.html