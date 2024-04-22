import json
import csv

# Function to flatten nested JSON
def flatten_json(json_obj, parent_key='', sep='_'):
    items = {}
    for key, value in json_obj.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, dict):
            items.update(flatten_json(value, new_key, sep=sep))
        else:
            items[new_key] = value
    return items

# Load JSON data from file
with open('metrics.out', 'r') as file:
    json_data = file.readlines()

# Initialize CSV writer
with open('net.csv', 'w', newline='') as csvfile:
    fieldnames = ['timestamp']
    for line in json_data:
        # Parse JSON
        data = json.loads(line)
        flattened_data = flatten_json(data['fields'])
        # Update fieldnames
        fieldnames.extend(flattened_data.keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Write data to CSV
    for line in json_data:
        data = json.loads(line)
        flattened_data = flatten_json(data['fields'])
        row = {'timestamp': data['timestamp']}
        for key in fieldnames[1:]:
            row[key] = flattened_data.get(key, 'null')
        writer.writerow(row)

print("CSV conversion completed.")
