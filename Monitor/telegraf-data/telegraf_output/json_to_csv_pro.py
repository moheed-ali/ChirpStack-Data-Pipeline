import json
import csv

# Open input and output files
with open('metrics.out', 'r') as infile, open('pro.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)

    # Write header row
    writer.writerow(['timestamp', 'blocked', 'dead', 'idle', 'paging', 'running', 'sleeping', 'stopped', 'total', 'total_threads', 'unknown', 'zombies'])

    # Process each line (JSON object) in the input file
    for line in infile:
        # Parse JSON
        data = json.loads(line)

        # Extract timestamp and fields
        timestamp = data['timestamp']
        fields = data['fields']

        # Write values to CSV row
        writer.writerow([
            timestamp,
            fields.get('blocked', None),
            fields.get('dead', None),
            fields.get('idle', None),
            fields.get('paging', None),
            fields.get('running', None),
            fields.get('sleeping', None),
            fields.get('stopped', None),
            fields.get('total', None),
            fields.get('total_threads', None),
            fields.get('unknown', None),
            fields.get('zombies', None)
        ])
