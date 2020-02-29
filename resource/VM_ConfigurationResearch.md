**Introduction**

Amazon EC2 provides a wide selection of instance types optimized to fit different use cases.
Instance types comprise varying combinations of CPU, memory, storage, and networking capacity and give you the flexibility to choose the appropriate mix of resources for your applications. 
Each instance type includes one or more instance sizes, allowing you to scale your resources to the requirements of your target workload.

**Types of Instances**

1. **_General Purpose:_** General purpose instances provide a balance of compute, memory and networking resources, and can be used for a variety of diverse workloads. These instances are ideal for applications that use these resources in equal proportions such as web servers and code repositories. 

    <br>Some examples of this are:</br>
      1. **A1 instances** have 1-16 vCPU's, ranging from 2-32 GiB of RAM, with Elastic Block Store (EBS) for storage. Network performance upto 10 Gbps is available.

      2. **M4 instances** provide a balance of compute, memory, and network resources, and it is a good choice for many applications. They have 
      2.3 GHz Intel Xeon® E5-2686 v4 (Broadwell) processors or 2.4 GHz Intel Xeon® E5-2676 v3 (Haswell) processors. EBS is optimized by default at no additional cost. RAM ranges from 8 - 256 GiB, having vCPU's between 2-64.

2. **_Compute Optimized:_**  Ideal for compute bound applications that benefit from high performance processors. Instances belonging to this family are well suited for batch processing workloads, media transcoding, high performance web servers, high performance computing (HPC), scientific modeling, dedicated gaming servers and ad server engines, machine learning inference and other compute intensive applications.

    <br>Some examples of this are:</br>
     1. **C4 instances** have high frequency Intel Xeon E5-2666 v3 (Haswell) processors optimized specifically for EC2. Default EBS-optimized for increased storage performance at no additional cost.
     Higher networking performance with Enhanced Networking supporting Intel 82599 VF. RAM ranges from 3.75 - 60 GiB. They also have dedicated EBS Bandwidth ranging between 500 - 4000 Mbps.

3.  **_Memory Optimized:_**   They are designed to deliver fast performance for workloads that process large data sets in memory.

    <br>Some examples of this are:</br>
     1. **z1d instances** offer both high compute capacity and a high memory footprint. High frequency z1d instances deliver a sustained all core frequency of up to 4.0 GHz, the fastest of any cloud instance.
     A custom Intel® Xeon® Scalable processor with a sustained all core frequency of up to 4.0 GHz.Up to 1.8TB of instance storage.Powered by the AWS Nitro System, a combination of dedicated hardware and lightweight hypervisor.With z1d instances, local NVMe-based SSDs are physically connected to the host server and provide block-level storage that is coupled to the lifetime of the z1d instance.High memory with up to 384 GiB of RAM.

4.  **_Accelerated Optimized:_** Instances use hardware accelerators, or co-processors, to perform functions, such as floating point number calculations, graphics processing, or data pattern matching, more efficiently than is possible in software running on CPUs.

    <br>Some examples of this are:</br>
     1. **p3 instances** are the latest generation of general purpose GPU instances.Up to 8 NVIDIA Tesla V100 GPUs, each pairing 5,120 CUDA Cores and 640 Tensor Cores.High frequency Intel Xeon E5-2686 v4 (Broadwell) processors for p3.2xlarge, p3.8xlarge, and p3.16xlarge.
      High frequency 2.5 GHz (base) Intel Xeon P-8175M processors for p3dn 24xlarge.Supports NVLink for peer-to-peer GPU communication.Provides up to 100 Gbps of aggregate network bandwidth.EFA support on p3dn.24xlarge instances.

5.  **_Storage Optimized:_** Instances are designed for workloads that require high, sequential read and write access to very large data sets on local storage. They are optimized to deliver tens of thousands of low-latency, random I/O operations per second (IOPS) to applications.

    <br>Some examples of this are:</br>
     1. **I3 instances** provide Non-Volatile Memory Express (NVMe) SSD-backed instance storage optimized for low latency, very high random I/O performance, high sequential read throughput and provide high IOPS at a low cost. I3 also offers Bare Metal instances (i3.metal), powered by the Nitro System, for non-virtualized workloads, workloads that benefit from access to physical resources, or workloads that may have license restrictions.High Frequency Intel Xeon E5-2686 v4 (Broadwell) Processors with base frequency of 2.3 GHz.Up to 25 Gbps of network bandwidth using Elastic Network Adapter (ENA)-based Enhanced Networking.High Random I/O performance and High Sequential Read throughput.Support bare metal instance size for workloads that benefit from direct access to physical processor and memory. RAM ranges from 15.25 - 512 GiB, with local storage ranging from 1 x 475 NVMe SSD - 8 x 1900 NVMe SSD.



A comprehensive list of different configurations of instances that are availble can be found here : https://aws.amazon.com/ec2/instance-types/#Intel
     
