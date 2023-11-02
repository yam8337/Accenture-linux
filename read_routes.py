import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# Load the XML file
tree = ET.parse('InTAS_005.rou.xml')
root = tree.getroot()

# Initialize a list to store departure times
departure_times = []

# Iterate over each vehicle element
for vehicle in root.findall('.//vehicle'):
    depart_time = float(vehicle.get('depart'))
    departure_times.append(depart_time)

# Create a histogram
plt.hist(departure_times, bins=20, color='blue', edgecolor='black')
plt.xlabel('Departure Time')
plt.ylabel('Number of Vehicles')
plt.title('Number of Vehicles Departing at Each Time Stamp')
plt.show()
