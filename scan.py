import scapy
from scapy.all import *
#import getmac
import os
import json

my_ip = socket.gethostbyname(socket.gethostname())
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
