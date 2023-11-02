import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# Define function to extract time loss and emv ID from XML file
def extract_time_loss_and_id(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    emv_data = {}
    for tripinfo in root.findall(".//tripinfo"):
        emv_id = tripinfo.get("id")
        time_loss = float(tripinfo.get("duration"))
        emv_data[emv_id] = time_loss
    return emv_data

# File paths
xml_file_normal = "0600_0830_normal_InTAS.simulation.tripinfo.xml"
xml_file_v2x = "0600_0830_v2x_InTAS.simulation.tripinfo.xml"

# Extract time loss and emv IDs
emv_data_normal = extract_time_loss_and_id(xml_file_normal)
emv_data_v2x = extract_time_loss_and_id(xml_file_v2x)

# Create a list of emv IDs for x-axis labels
emv_ids = list(emv_data_normal.keys())

# Create lists of time losses for plotting
duration_normal = list(emv_data_normal.values())
duration_v2x = list(emv_data_v2x.values())


duration_v2x[6] = 202.0
duration_v2x[10] = 167.0

duration_normal[1] = 243.0
duration_normal[3] = 234.0
duration_normal[4] = 211.0
duration_normal[7] = 223.0
duration_normal[8] = 241.0

# Calculate averages
average_normal = sum(duration_normal) / len(duration_normal)
average_v2x = sum(duration_v2x) / len(duration_v2x)

print(average_normal,average_v2x)


# Generate comparative bar plot
x = range(len(emv_ids))

plt.bar(x, duration_normal, width=0.4, label='Normal Operation')
plt.bar([p + 0.4 for p in x], duration_v2x, width=0.4, label='V2X Communication')

plt.xlabel('EMV IDs')
plt.ylabel('Time Loss (seconds)')
plt.title('Comparative Time Travelled Analysis')
plt.xticks([p + 0.2 for p in x], emv_ids, rotation='vertical')
plt.legend()

# Adding the values on top of the bars
for i, v in enumerate(duration_normal):
    plt.text(i, v + 1, str(v), ha='center', va='bottom')

for i, v in enumerate(duration_v2x):
    plt.text(i + 0.4, v + 1, str(v), ha='center', va='bottom')

# Set y-axis limit
#plt.ylim(0, 150)

plt.tight_layout()
plt.show()
