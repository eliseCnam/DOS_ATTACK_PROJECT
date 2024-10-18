#--------------------------------------------------------------
#                   display_analyze.py
#--------------------------------------------------------------
# This file displays the analyzes of the attack.

import matplotlib
matplotlib.use('Agg') # prevent matplotlib from trying to open any graphical windows and instead render the plots off-screen
import matplotlib.pyplot as plt
import analyze_data as analyze
import analyze_ip_loc as analyze_loc
import webbrowser


########################################
#          Run the analysis
########################################

# Perform analysis for attack packets, bytes, and bytes per second
analyze.analyze_attack_more_packets()
analyze.analyze_attack_largest_traffic()
analyze.analyze_attack_largest_bytes_per_second()

# Perform analysis for IP locations
analyze_loc.analyze_ip_location()


print(f"The attack that generated the most packets: {analyze.getMostPacketsAttack()['Attack Type']} with {analyze.getMostPacketsAttack()['Packet Count']} packets")
print(f"The attack that generated the largest traffic: {analyze.getMostBytesAttack()['Attack Type']} with {analyze.getMostBytesAttack()['Packet Size']} bytes")
print(f"The attack that generated the largest traffic in bytes per second: {analyze.getMostBytesPerSecAttack()['Attack Type']} with {analyze.getMostBytesPerSecAttack()['Bytes per Second']} bytes per second")

############################################################
#                      Plot the Results
############################################################
# Plot ip location
plt_map = analyze_loc.plot_locations_on_map()
plt_map.title("IP location")
plt_map.savefig('./Plot_analyze/plot_locations.png')
plt_map.show()


# Plot number of packets per attack type
plt.figure(figsize=(10, 6))
plt.bar(analyze.getAttackPacketCounts()['Attack Type'], analyze.getAttackPacketCounts()['Packet Count'])
plt.xlabel('Attack Type')
plt.ylabel('Number of Packets')
plt.title('Number of Packets per Attack Type')
plt.xticks(rotation=45)
plt.savefig('./Plot_analyze/plot_packets.png')
plt.show()

# Plot total bytes per attack type
plt.figure(figsize=(10, 6))
plt.bar(analyze.getAttackByteCounts()['Attack Type'], analyze.getAttackByteCounts()['Packet Size'], color='green')
plt.xlabel('Attack Type')
plt.ylabel('Total Bytes')
plt.title('Total Bytes per Attack Type')
plt.xticks(rotation=45)
plt.savefig('./Plot_analyze/plot_bytes.png')
plt.show()

# Plot bytes per second per attack type
plt.figure(figsize=(10, 6))
plt.bar(analyze.getAttackTrafficPerSec()['Attack Type'], analyze.getAttackTrafficPerSec()['Bytes per Second'], color='red')
plt.xlabel('Attack Type')
plt.ylabel('Bytes per Second')
plt.title('Bytes per Second per Attack Type')
plt.xticks(rotation=45)
plt.savefig('./Plot_analyze/plot_bytes_sec.png')
plt.show()