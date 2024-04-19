import json
import csv

# Function to convert JSON data to CSV
def json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = f.readlines()

    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)

        # Write the header
        header = ["timestamp", "cpu", "usage_guest", "usage_guest_nice", "usage_idle", 
                  "usage_iowait", "usage_irq", "usage_nice", "usage_softirq", 
                  "usage_steal", "usage_system", "usage_user"]
        writer.writerow(header)

        # Convert JSON to CSV rows
        for line in data:
            row = json.loads(line)
            timestamp = row['timestamp']
            cpu = row['tags']['cpu']
            fields = row['fields']
            csv_row = [timestamp, cpu]
            for key in header[2:]:
                csv_row.append(fields.get(key, "null"))  # Replace missing values with "null"
            writer.writerow(csv_row)

# Usage
json_to_csv('data.out', 'data.csv')
