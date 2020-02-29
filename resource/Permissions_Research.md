***********************IP ADDRESS AND PORT REQUIREMENTS FOR AMAZON WORKSPACES***********************

PORT 443 (TCP) : This port is used to register, authenticate, update the client application.
                 This port is open with AMAZON and S3 subset in various regions.

Port 4172 (UDP and TCP) : This is used in streaming the health checks and WorkSpace desktop. It 
                          is to be open to the PCoIP Gateway IP address ranges.
                         
Ports for Web Access : 
Port 53 (UDP) : This port is used by the DNS servers and must be open to your DNS server IP 
                addresses which helps the client in resolving the public domain names.

Port 80 (UDP and TCP) :  This port switches to HTTPS after establishing the connections to 
                         https://clients.amazonworkspaces.com.
                   
Port 443 (UDP and TCP) : This port is used for registration and authentication using HTTPS.

UDP is preferred over TCP for desktop streams, but sometimes uses TCP if UDP is not available.
If all the UDP ports are blocked except 53, 80, 443, Web Access will work on Chrome and Firefox
using TCP connections.

Reference: 
https://docs.aws.amazon.com/workspaces/latest/adminguide/workspaces-port-requirements.html