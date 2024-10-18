#--------------------------------------------------------------
#                   get_ip_locations.py
#--------------------------------------------------------------
# This file is used to get the location of the DOS attacker.

import requests
import analyze_data as analyze

# Function to get the location of an IP address
def get_ip_location(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        return {'lat': data['lat'], 'lon': data['lon'], 'country': data['country']}
    except:
        return {'lat': None, 'lon': None, 'country': 'Unknown'}

# Get a list of unique suspect IP addresses
suspect_ips = analyze.getData()['Source IP'].unique()

# Get the locations for each IP
__locations = {ip: get_ip_location(ip) for ip in suspect_ips}

def get_locations():
    return __locations