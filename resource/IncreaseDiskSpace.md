**Increase hard disk space of EC2 instance on the go**

***Steps***

1. Login to AWS console.

2. Go to Elastic Block Storage (EBS). 
3. Right click on the instance you wish to resize.
4. Click on "Modify Volume"
5. Enter desired size in "SIze" field and click Modify button.
6. Ssh into the instance and resize the partition using the following steps.
7. Enter the command "lsblk" to list the block devices attached.
8. Based on what you see from step 7, resize the partiton using the following commands, \
        a. sudo growpart /dev/xvda 1 (assuming xvda1 is the partition. Enter your corresponding one here) \
        b. sudo resize2fs /dev/xvda1
9. Finally, check the disk size using the command df -h.