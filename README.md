SRX Firewall - Dynamic entry of User parameters
===============================================
The SRX firewall can be configured to inspect a network users name and role in the network as part of Firewall policy. Typically this is done through integration with LDAP or Active Directory. There is also the ability to statically define users from the CLI or through the Netconf API. This simple script allows a remote user or system to automate the process of adding/deleting users. 

Usage 
=====


Adding a user called Fred with the IP address of 10.0.0.1 as a guest user 
```
user@server:~# ./update-userfw.py add fred 10.0.0.1 guest 
```

Deleting the user called Fred and all associated attributes 

```
user@server:~# ./update-userfw.py del fred
``


SRX Junos CLI commands 
======================

Summary view of all statically defined users. 
```
admin@SRX220> show security user-identification local-authentication-table all    
Total entries: 10
Source IP       Username     Roles
10.0.0.1        fred         guest                           
```

Detailed view of an individaul user. 

```
admin@SRX220> show security user-identification local-authentication-table user fred 
Total entries: 1
Ip-address: 10.0.0.1
Username: fred
Roles: guest
```

