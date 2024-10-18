#--------------------------------------------------------------
#                   analyze_ip_loc.py
#--------------------------------------------------------------
# This file analyzes the ip's location to display them.
# They're 2 types of display : dynamic map (html) and on a map image (basemap)

import folium as folium
import matplotlib.pyplot as plt
import get_ip_locations as iploc
from mpl_toolkits.basemap import Basemap

''' Analyze the IP location of the attacks and draw them on a dynamic map (html)'''
def analyze_ip_location():

    locations = iploc.get_locations()

    world_map = folium.Map(location=[20, 0], zoom_start=2)          # Create a map

    for ip, loc in locations.items():                               # Loop over the locations and add markers to the map
        lat = loc['lat']
        lon = loc['lon']
        country = loc['country']
        
        if lat and lon:                                             # Only add marker if the location is valid
            folium.Marker(
                location=[lat, lon],
                popup=f"IP: {ip}<br>Country: {country}",
                icon=folium.Icon(color='blue')
            ).add_to(world_map)

    world_map.save('./Plot_analyze/suspect_ips_map.html')

def plot_locations_on_map():

    locations = iploc.get_locations()
    
    m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c')

    # Draw coastlines, countries, and map boundaries
    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary()

    for ip, loc in locations.items():
        lat = loc['lat']
        lon = loc['lon']
        country = loc['country']

        if lat and lon :
            x, y = m(lon, lat)
            m.plot(x, y, 'ro', markersize=5)                       # Plot points as red circles
    
    return plt
