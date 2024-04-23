import json
import csv

# Open input and output files
with open('metrics.out', 'r') as infile, open('swap.csv', 'w', newline='') as outfile:
    # Create a CSV writer object
    writer = csv.writer(outfile)

    # Write the header row
    writer.writerow(['timestamp', 'name', 'host', 'free', 'total', 'used', 'used_percent', 'in', 'out'])

    # Iterate over each line in the input file
    for line in infile:
        # Load JSON data from each line
        data = json.loads(line)

        # Extract values from JSON data or set them to None if they don't exist
        timestamp = data.get('timestamp')
        name = data.get('name')
        host = data['tags'].get('host')
        fields = data.get('fields', {})
        free = fields.get('free')
        total = fields.get('total')
        used = fields.get('used')
        used_percent = fields.get('used_percent')
        swap_in = fields.get('in')
        swap_out = fields.get('out')

        # Write the values to the CSV file
        writer.writerow([timestamp, name, host, free, total, used, used_percent, swap_in, swap_out])
