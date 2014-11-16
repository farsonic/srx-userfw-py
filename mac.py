#!/usr/bin/python

import sys
from jnpr.junos import Device





dev = Device(host='192.168.0.2',gather_facts='False',user='admin',password='jun1per')
dev.open()
if (sys.argv[1]=='add') or (sys.argv[1]=='old'): 
   cmd = dev.rpc.request_userfw_local_auth_table_add(user_name=str(sys.argv[2]),ip_address=str(sys.argv[3]),roles=str(sys.argv[4]))
if sys.argv[1]=='del':
    cmd = dev.rpc.request_userfw_local_auth_table_delete_user(user_name=str(sys.argv[2]))
dev.close()


