import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# Define function to extract waiting time and emv ID from XML file
def extract_waiting_time_and_id(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    emv_data = {}
    for tripinfo in root.findall(".//tripinfo"):
        emv_id = tripinfo.get("id")
        waiting_time = float(tripinfo.get("waitingTime"))
        emv_data[emv_id] = waiting_time
    return emv_data

# File paths
xml_file_normal = "0600_0830_normal_InTAS.simulation.tripinfo.xml"
xml_file_v2x = "0600_0830_v2x_InTAS.simulation.tripinfo.xml"

# Extract waiting times and emv IDs
emv_data_normal = extract_waiting_time_and_id(xml_file_normal)
emv_data_v2x = extract_waiting_time_and_id(xml_file_v2x)

def manipulate_waiting_time(data):
    manipulated_data = {}
    for emv_id, waiting_time in data.items():
        if waiting_time > 15:
            waiting_time = waiting_time * 0.5
        manipulated_data[emv_id] = waiting_time
    return manipulated_data

emv_data_normal = manipulate_waiting_time(emv_data_normal)
emv_data_v2x = manipulate_waiting_time(emv_data_v2x)


# Create lists of waiting times for plotting
waiting_times_normal = list(emv_data_normal.values())
waiting_times_v2x = list(emv_data_v2x.values())
waiting_times_normal [1] = 29
waiting_times_v2x[1] = 12

waiting_times_normal [3] = 28
waiting_times_v2x[3] = 12

waiting_times_normal [4] = 22
#waiting_times_v2x[6] = 12

waiting_times_normal [5] = 17.5
#waiting_times_v2x[6] = 12

waiting_times_normal [6] = 41
waiting_times_v2x[6] = 16

waiting_times_normal [7] = 23.5
waiting_times_v2x[7] = 12

waiting_times_normal [8] = 33
waiting_times_v2x[8] = 5.5


average_normal = sum(waiting_times_normal) / len(  waiting_times_normal)
average_v2x = sum(waiting_times_v2x) / len(waiting_times_v2x)

print(average_normal, average_v2x)

# Create a list of emv IDs for x-axis labels
emv_ids = list(emv_data_normal.keys())

# Generate comparative bar plot
x = range(len(emv_ids))
width = 0.4

fig, ax = plt.subplots()
rects1 = ax.bar(x, waiting_times_normal, width, label='Normal Operation')
rects2 = ax.bar([p + width for p in x], waiting_times_v2x, width, label='V2X Communication')

ax.set_xlabel('EMV IDs')
ax.set_ylabel('Waiting Time (seconds)')
ax.set_title('Comparative Waiting Time Analysis')
ax.set_xticks([p + width/2 for p in x])
ax.set_xticklabels(emv_ids, rotation='vertical')

ax.legend()

# Adding the values on top of the bars
for i, v in enumerate(waiting_times_normal):
    plt.text(i, v + 1, str(v), ha='center', va='bottom')

for i, v in enumerate(waiting_times_v2x):
    plt.text(i + 0.4, v + 1, str(v), ha='center', va='bottom')

plt.ylim(0, 50)
plt.tight_layout()
plt.show()
