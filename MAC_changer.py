#!/usr/bin/env python

import subprocess
import argparse
import re

parser = argparse.ArgumentParser(description="mac_addr to change")
parser.add_argument('interface',type=str,help="enter the interface aka dev")
parser.add_argument('new_mac_addr',type=str,help="enter new mac_addr")
args=parser.parse_args()

def change_mac(iface,new_mac):
    subprocess.run(["sudo", "ip", "link", "set", "dev", iface, "down"])
    payload="sudo ip link set dev "+iface+" address "+ new_mac
    subprocess.run(payload, shell=True)
    subprocess.run(["sudo", "ip", "link", "set", "dev", iface, "up"])
    #subprocess.run("ip link", shell=True)
    
def get_mac(iface):
    ip_result=subprocess.run(["ip","addr","list",iface],stdout=subprocess.PIPE,encoding='utf-8')
    mac_res=re.search(r'(\w\w:){5}\w\w',ip_result.stdout)
    if mac_res:
        return mac_res.group(0)
    else:
        print("dev has no MAC address")

current_mac=get_mac(args.interface)
print('previous MAC is = ',str(current_mac))
change_mac(args.interface,args.new_mac_addr)

current_mac=get_mac(args.interface)
if current_mac == args.new_mac_addr:
    print('MAC address was successfully changed to ' + args.new_mac_addr)
else:
    print('failed to change MAC address')
