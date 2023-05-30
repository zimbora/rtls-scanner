import time
import signal
import sys
from scapy.all import *
import subprocess
from src.network import networkHTTP
import platform

# Get the operating system name
os_name = platform.system()
ssid = ""
router_mac = ""
map_id = None

# Print the detected operating system
print("Operating System:", os_name)

http = networkHTTP()

device = {}

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

## not used
def get_router_mac():
    cmd =["nmcli -f BSSID,ACTIVE dev wifi list | awk '$2 ~ /yes/ {print $1}'"]
    address = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = address.communicate()
    return out.decode('ascii').replace('\n','')

def get_connected_ssid():
    global ssid
    if os_name != "Darwin":
        response = subprocess.run(['iwgetid'], capture_output=True, text=True).stdout.strip("\n")
        filter = "ESSID:"
        index = response.rfind(filter)+len(filter);
        last_ssid = ssid;
        ssid = response[index+1:len(response)-1]
    else:
        cmd = ["networksetup", "-getairportnetwork", "en0"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        ssid = res.stdout.split(": ")[1]
        print("ssid:",ssid)

def check_connected_AP():
    get_connected_ssid()
    wifi = http.getWifiCrendentials(map_id)
    if len(wifi) > 0:
        if wifi[0]['ssid'] != ssid:
            print("Not connected to correct AP !!")
            print("desired AP:",wifi[0]['ssid'])
            print("actual AP:",ssid)
            return False
        else: return True
    else: return False

signal.signal(signal.SIGINT, signal_handler)

while(True):
    # get submask net
    interfaces = [_if for _if in get_if_list() if _if not in ['lo', 'docker0']]
    addresses = [_addr for _addr in [ get_if_addr(_if) for _if in interfaces ] if _addr not in ['0.0.0.0', '127.0.1.1', '127.0.0.1']]
    my_ip = addresses[0]
    index = my_ip.rfind('.');
    mask = my_ip[0:index+1]

    if map_id != None and check_connected_AP():

        ans,unans = arping(mask+"1/24", verbose=0)
        for s,r in ans:
            mac = r[Ether].src
            ip = s[ARP].pdst

            print("{} {}".format(ip,mac))
            if ip in device and device[ip] == mac:
                #print("mac: {} already mapped".format(device[ip]))
                continue
            '''
            if ip in device:
                print("mac: {} not match {}".format(mac,device[ip]))
            else:
                print("mac: {} not found".format(mac))
            '''
            device[ip] = mac
            http.updateUserMapInfo(map_id,ip,mac,None)
    else:

        if http.getToken():
            floors = http.getFloors()

            if len(floors) > 0:
                map_id = floors[0]['id']
                print("map id:",map_id)

        else: print("api token not available")

        time.sleep(30)
