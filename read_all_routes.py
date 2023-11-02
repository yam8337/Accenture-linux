import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import os

# Define a directory containing your XML files
xml_dir = '/home/v2x/InTAS/scenario/routes/'

# Initialize a list to store all departure times
all_departure_times = []

# Iterate over each file in the directory
for filename in os.listdir(xml_dir):
    if filename.endswith('.xml'):
        # Load the XML file
        tree = ET.parse(os.path.join(xml_dir, filename))
        root = tree.getroot()

        # Initialize a list to store departure times for this file
        departure_times = []

        # Iterate over each vehicle element in this file
        for vehicle in root.findall('.//vehicle'):
            depart_time = float(vehicle.get('depart'))
            departure_times.append(depart_time)

        # Add the list of departure times for this file to the overall list
        all_departure_times.extend(departure_times)

# Convert departure times to hours
departure_times_hours = [time // 1800 for time in all_departure_times]

# Create a histogram
plt.hist(departure_times_hours, bins=48, range=(0, 48), color='blue', edgecolor='black')
#plt.hist(all_departure_times, bins=20, color='blue', edgecolor='black')
plt.xlabel('Departure Time')
plt.ylabel('Number of Vehicles')
plt.title('Number of Vehicles Departing(Every 30 min)')
#plt.xticks(range(0, 25, 1))  # Set x-axis ticks every hour
plt.xticks(range(0, 49, 1), [f'{i//2}:{(i%2)*3}0' for i in range(49)])

# Add labels on top of bars
for i, v in enumerate(plt.hist(departure_times_hours, bins=48, range=(0, 48), color='blue')[0]):
    plt.text(i, v + 5, str(int(v)), color='black', ha='left')

plt.show()
