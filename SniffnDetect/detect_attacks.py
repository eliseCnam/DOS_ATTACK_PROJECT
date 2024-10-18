#--------------------------------------------------------------
#                   detect_attacks.py
#--------------------------------------------------------------
# This file detects the DOS attacks and logs them in a CSV file.

import csv
import time
from sniffndetect import SniffnDetect

__csv_file = 'attack_log.csv'
csv_headers = ['Timestamp', 'Source IP', 'Destination IP', 'Protocol', 'Source Port', 'Destination Port', 'Attack Type', 'Packet Size']

def get_csv_file():
    return __csv_file

''' Initialize the CSV file by writting headers '''
def initialize_csv():
    with open(__csv_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(csv_headers)

''' Log each detected attack into the CSV '''
def log_attack_to_csv(pkt_time, src_ip, dst_ip, protocol, src_port, dst_port, attack_type, packet_size):
    with open(__csv_file, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([pkt_time, src_ip, dst_ip, protocol, src_port, dst_port, attack_type, packet_size])

''' Main: Initialize the file and start sniffing to detect the attacks and then add them to the CSV file '''
if __name__ == "__main__":
    
    initialize_csv()

    sniffer = SniffnDetect()
    sniffer.start()

    while True:
        # For each detected attack, log into the CSV
        for activity in sniffer.RECENT_ACTIVITIES:
            pkt_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(activity[0]))
            src_ip = activity[2]
            dst_ip = activity[3]
            protocol = ','.join(activity[1])
            src_port = activity[6]
            dst_port = activity[7]
            attack_type = activity[9]
            packet_size = activity[10] if activity[10] else 0

            # Only log if an attack type is detected
            if attack_type:
                log_attack_to_csv(pkt_time, src_ip, dst_ip, protocol, src_port, dst_port, attack_type, packet_size)
