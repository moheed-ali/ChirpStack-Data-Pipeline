import json
import csv

# Define input and output file paths
input_file = 'metrics.out'
output_file = 'sys.csv'

# Open input and output files
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    # Create a CSV writer
    csv_writer = csv.writer(outfile)

    # Write header row
    csv_writer.writerow(['timestamp', 'load1', 'load15', 'load5', 'n_cpus', 'uptime', 'uptime_format'])

    # Iterate over lines in the input file
    for line in infile:
        # Load JSON from each line
        data = json.loads(line)

        # Extract relevant fields
        timestamp = data.get('timestamp')
        fields = data.get('fields', {})
        tags = data.get('tags', {})
        
        # Initialize values
        load1 = fields.get('load1')
        load15 = fields.get('load15')
        load5 = fields.get('load5')
        n_cpus = fields.get('n_cpus')
        uptime = fields.get('uptime')
        uptime_format = fields.get('uptime_format')

        # Write row to CSV
        csv_writer.writerow([timestamp, load1, load15, load5, n_cpus, uptime, uptime_format])
