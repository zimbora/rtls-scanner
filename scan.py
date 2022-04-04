import scapy
from scapy.all import *
#import getmac
import os
import json

interfaces = [_if for _if in get_if_list() if _if not in ['lo', 'docker0']]
addresses = [_addr for _addr in [ get_if_addr(_if) for _if in interfaces ] if _addr not in ['0.0.0.0', '127.0.1.1', '127.0.0.1']]
my_ip = addresses[0]
index = my_ip.rfind('.');
mask = my_ip[0:index+1]

devices = []
i = 0
while i < 255:
    i += 1
    print("i:",i)
    ip = mask+str(i)
    try:
        response = os.system("fping -c 1 -t 250 " + ip)
        print(response)
        if response == 0:
            name = ""
            try:
                name = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                print(socket.herror)

            mac = getmacbyip(ip);
            #print("{} {} {}\n".format(mac,ip,name))
            obj = {
                "ip":ip,
                "name":name,
                "mac":mac
            }
            devices.append(obj)
        else:
          print(ip, 'is down!')
    except (socket.herror, socket.gaierror):
        #if getmacbyip(ip) != None:
            #print("{} {} \n".format(getmacbyip(ip),ip))
        continue

#print(devices)
for device in devices:
    print(device)

#ip = "10.168.1.160"
#domain_name = socket.gethostbyaddr(ip)[0]
#print(domain_name)

#print("{} {}".format(getmacbyip(ip),ip))
