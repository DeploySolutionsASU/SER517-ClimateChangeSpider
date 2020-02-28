**Introduction**

AWS Backup is a fully managed backup service that makes it easy to centralize and automate the backup of data across AWS services in the cloud and on premises. Using AWS Backup, you can configure backup policies and monitor backup activity for your AWS resources in one place.


**Supported Resources**

The following resources can be backed up and restored using AWS Backup:

1. Amazon Elastic File System (EFS): Amazon EFS file systems can be backed up and restored.

2. Amazon DynamoDB (Tables)

3. Amazon EC2 instances

4. Amazon EBS volumes

5. Amazon RDS databases

6. AWS Storage Gateway volumes


**Configuring Amazon EC2 instance Backup**

**_How it works?_**

Using AWS Backup, you can schedule or perform on-demand backup jobs that include entire EC2 instances, along with associated configuration data. This limits the need for you to interact with the storage (Amazon EBS) layer. Similarly, you can restore an entire Amazon EC2 instance from a single
recovery point.

When backing up an Amazon EC2 instance, AWS Backup takes a snapshot of the root Amazon EBS storage volume, the launch configurations, and all associated EBS volumes. AWS Backup stores certain configuration parameters of the EC2 instance, including instance type, security groups, Amazon VPC,
monitoring configuration, and tags. The backup data is stored as an Amazon EBS volume-backed AMI
(Amazon Machine Image).

**_Steps:_**

1. Sign in to your AWS account to open the AWS console.

2. Select Services in the top bar and click EC2 to launch the EC2 Management Console.

3. Select Running Instances and choose the instance you would like to back up.

4. In the bottom pane, you can view the central technical information about the instance. In the Description tab, find the Root device section and select the /dev/sda1 link.

5. In the pop-up window, find the volume’s EBS ID name and click it.

6. The Volumes section should open. Click Actions and select Create Snapshot.

7. The Create Snapshot box should open, where you can add a description for the snapshot to make it distinct from other snapshots, as well as assign tags to easily monitor this snapshot. Click Create Snapshot.

8. The snapshot creation should start and be completed in a minimal amount of time. The main factor here is the size of data in your Amazon EBS volume.

After the snapshot creation is complete, you can find your new snapshot by selecting the Snapshots section in the left pane. This indicates that the snapshot creation is successful and has created a point-in-time copy of the EBS volume, which can later be used to restore your EC2 instance.

It is worth noting that, this is just one of many approaches that can be used for backing up Amazon EC2 instances.

**Pricing**

| Resource Type  | Warm Storage|
| ------------- | ------------- |
| Amazon EFS File System Backup  |  $0.06 per GB-Month |
| Amazon EBS Volume Snapshot | $0.055 per GB-Month  |
| Amazon RDS Database Snapshot | $0.095 per GB-Month  |
| Amazon DynamoDB Table Backup	 | $0.112 per GB-Month  |
| AWS Storage Gateway Volume Backup	 | $0.055 per GB-Month  |


**References**

1. Amazon Backup Developer Guide : https://docs.aws.amazon.com/aws-backup/latest/devguide/AWSBackup-dg.pdf#api-reference

2. https://www.nakivo.com/blog/perform-aws-ec2-backup-step-step-guide/

3. https://aws.amazon.com/backup/pricing/