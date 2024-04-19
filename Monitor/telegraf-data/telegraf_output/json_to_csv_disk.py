import json
import csv

# Define the input and output file paths
input_file = 'metrics.out'
output_file = 'disk.csv'

# Function to handle missing keys by returning None
def get_field(obj, key):
    return obj.get(key, None)

# Read JSON lines from input file and write to CSV
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    
    # Write the header row
    writer.writerow(['timestamp', 'free', 'inodes_free', 'inodes_total', 'inodes_used', 'inodes_used_percent', 'total', 'used', 'used_percent', 'name', 'device', 'fstype', 'host', 'mode', 'path'])
    
    for line in infile:
        data = json.loads(line)
        
        # Extract relevant fields
        timestamp = data['timestamp']
        fields = data.get('fields', {})
        tags = data.get('tags', {})
        
        # Write a row to CSV with appropriate field values or None if not present
        writer.writerow([
            timestamp,
            get_field(fields, 'free'),
            get_field(fields, 'inodes_free'),
            get_field(fields, 'inodes_total'),
            get_field(fields, 'inodes_used'),
            get_field(fields, 'inodes_used_percent'),
            get_field(fields, 'total'),
            get_field(fields, 'used'),
            get_field(fields, 'used_percent'),
            data.get('name', None),
            tags.get('device', None),
            tags.get('fstype', None),
            tags.get('host', None),
            tags.get('mode', None),
            tags.get('path', None)
        ])
