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
```


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

SRX Security Policy enforcement 
===============================
The SRX can leverage both the username and the role assignment as part of security policy. This allows the policy to allow any authenticated user, or individual users and/or their roles. An example policy to only let the "fred" user through the firewall between the trust and untrust zone. 

```
[edit security policies from-zone trust to-zone untrust]
admin@SRX220# show 
policy allow-fred {
    match {
        source-address any;
        destination-address any;
        application any;
        source-identity fred;
    }
    then {
        permit;
        log {
            session-init;
            session-close;
        }
    }
}
```

Example Usage (Integration with DNSMASQ) 
========================================

This script was originally created to be used with the DNSMASQ DHCP server but can also function as a standalone script. DNSMASQ when operating as a DHCP server can exectute a script for the addition (add) or removal (del) of a users lease. When DNSMASQ executes a script it will always pass the following arguments to the script for processing 
```
* argument1 add/del/old 
* argument2 MAC-Address
* argument3 Assigned IP Address
* argument4 DHCP Client Name (received during DHCP Request) 
```

For integration between DNSMASQ and the SRX userfw feature we are assoicating the username with MAC Address, IP-address with the users IP-Address and DHCP Client-ID with the users role. Note, it is also possible to execute the script multple times for the same user and keep assigning multiple roles.  

In order to integrate the above script into your DNSMASQ enviroment add the following configuration entry into your /etc/dnsmasq.conf file

```
dhcp-script=/path/to/update-userfw.py
```


SRX Operational mode output
===========================
```
admin@SRX220> show security user-identification local-authentication-table all                    
Total entries: 8
Source IP       Username     Roles
192.168.0.130   6c:ad:f8:52: Chromecast                      
192.168.0.131   14:10:9f:ee: Ipad-1
192.168.0.132   10:ae:60:08: android-1234
192.168.0.138   8c:7b:9d:e8: iPad0231                            
192.168.0.141   e4:ce:8f:40: Macbook-Pro
192.168.0.143   b8:27:eb:93: raspberrypi                     
192.168.0.145   10:bf:48:e8: android-baadabb10f5eef53        
192.168.0.149   b0:34:95:2a: Windows-XYZ
```

With the above script in place and operational, users details will be dynamically added and removed from the local authentication table. With the correct firewall policy in place and logging enabled all events will be recording to include the users MAC-Address, IP-Address, Username and role. This would be specifically useful in an uncontrolled environment were records need to be kept of user activity and there is no ability to intergrate a wider userfw intagration with Active Directory. 
