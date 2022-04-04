import signal
import sys
from scapy.all import *
import subprocess
from src.network import networkHTTP

http = networkHTTP()

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def Check_connected_ap():
    cmd =["nmcli -f BSSID,ACTIVE dev wifi list | awk '$2 ~ /yes/ {print $1}'"]
    address = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = address.communicate()
    return out.decode('ascii').replace('\n','')

signal.signal(signal.SIGINT, signal_handler)
while(True):
    # get submask net
    interfaces = [_if for _if in get_if_list() if _if not in ['lo', 'docker0']]
    addresses = [_addr for _addr in [ get_if_addr(_if) for _if in interfaces ] if _addr not in ['0.0.0.0', '127.0.1.1', '127.0.0.1']]
    my_ip = addresses[0]
    index = my_ip.rfind('.');
    mask = my_ip[0:index+1]

    # get router mac address
    #router_mac = getmacbyip(mask+"1")
    router_mac = Check_connected_ap()
    print(router_mac)

    # get network ssid
    response = subprocess.run(['iwgetid'], capture_output=True, text=True).stdout.strip("\n")
    filter = "ESSID:"
    index = response.rfind(filter)+len(filter);
    ssid = response[index+1:len(response)-1]
    #ssid = "Vodafone-rocks"
    print("ssid:",ssid)

    map_id = http.getMap(router_mac,ssid)
    print("map_id: ",map_id)

    ans,unans = arping(mask+"1/24", verbose=0)
    for s,r in ans:
        mac = r[Ether].src
        ip = s[ARP].pdst
        http.updateUserMapInfo(map_id,ip,mac,None)
        print("{} {}".format(ip,mac))
