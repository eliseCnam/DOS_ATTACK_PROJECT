#--------------------------------------------------------------
#                   analyze_data.py
#--------------------------------------------------------------
# This file analyzes the attack log CSV file.

import pandas as pd
import detect_attacks as da

__data = pd.read_csv(da.get_csv_file(), delimiter=";")      # Load the data
__data.head()                                               # Display the first few rows of the data
__attack_packet_counts = pd.DataFrame()
__most_packets_attack = pd.DataFrame()
__attack_byte_counts = pd.DataFrame()
__most_bytes_attack = pd.DataFrame()
__attack_traffic_per_sec = pd.DataFrame()
__most_bytes_per_sec_attack = pd.DataFrame()

def getData() :
    return __data

def getAttackPacketCounts() :
    global __attack_packet_counts
    return __attack_packet_counts

def getMostPacketsAttack():
    global __most_packets_attack
    return __most_packets_attack

def getAttackByteCounts():
    global __attack_byte_counts
    return __attack_byte_counts

def getMostBytesAttack():
    global __most_bytes_attack
    return __most_bytes_attack

def getAttackTrafficPerSec():
    global __attack_traffic_per_sec
    return __attack_traffic_per_sec

def getMostBytesPerSecAttack():
    global __most_bytes_per_sec_attack
    return __most_bytes_per_sec_attack


''' Analyze the Attack That Generated More Packets '''
def analyze_attack_more_packets():
    global __attack_packet_counts
    global __most_packets_attack
    # Group by attack type and count packets (number of rows per attack)
    __attack_packet_counts = __data.groupby('Attack Type').size().reset_index(name='Packet Count')

    # Find the attack that generated the most packets
    __most_packets_attack = __attack_packet_counts.loc[__attack_packet_counts['Packet Count'].idxmax()]


''' Analyze the Attack That Generated the Largest Traffic (in Bytes) '''
def analyze_attack_largest_traffic():
    global __attack_byte_counts
    global __most_bytes_attack
    # Convert 'Packet Size' to numeric, ignoring non-numeric entries
    __data['Packet Size'] = pd.to_numeric(__data['Packet Size'], errors='coerce')

    # Group by attack type and sum the packet sizes (bytes)
    __attack_byte_counts = __data.groupby('Attack Type')['Packet Size'].sum().reset_index()

    # Find the attack that generated the most traffic
    __most_bytes_attack = __attack_byte_counts.loc[__attack_byte_counts['Packet Size'].idxmax()]



''' Analyze the Attack With the Largest Bytes per Second '''
def analyze_attack_largest_bytes_per_second():

    global __attack_traffic_per_sec
    global __most_bytes_per_sec_attack

    # Parse 'Timestamp' as datetime
    __data['Timestamp'] = pd.to_datetime(__data['Timestamp'])

    # Calculate duration of each attack type
    attack_duration = __data.groupby('Attack Type').apply(lambda x: (x['Timestamp'].max() - x['Timestamp'].min()).total_seconds()).reset_index(name='Duration')

    # Merge with byte counts
    __attack_traffic_per_sec = pd.merge(__attack_byte_counts, attack_duration, on='Attack Type')

    # Calculate bytes per second for each attack
    __attack_traffic_per_sec['Bytes per Second'] = __attack_traffic_per_sec['Packet Size'] / __attack_traffic_per_sec['Duration']

    # Find the attack with the highest bytes per second
    __most_bytes_per_sec_attack = __attack_traffic_per_sec.loc[__attack_traffic_per_sec['Bytes per Second'].idxmax()]
