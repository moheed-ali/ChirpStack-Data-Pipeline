import json
import csv

input_file = 'metrics.out'
output_file = 'diskio.csv'

# Define the fieldnames for the CSV
fieldnames = ['timestamp', 'name', 'host', 'wwid', 'io_time', 'iops_in_progress', 'merged_reads',
              'merged_writes', 'read_bytes', 'read_time', 'reads', 'weighted_io_time',
              'write_bytes', 'write_time', 'writes']

with open(input_file, 'r') as in_file, open(output_file, 'w', newline='') as out_file:
    writer = csv.DictWriter(out_file, fieldnames=fieldnames)
    writer.writeheader()

    for line in in_file:
        data = json.loads(line)
        fields = data.get('fields', {})
        tags = data.get('tags', {})
        
        row = {
            'timestamp': data.get('timestamp'),
            'name': data.get('name'),
            'host': tags.get('host'),
            'wwid': tags.get('wwid'),
            'io_time': fields.get('io_time'),
            'iops_in_progress': fields.get('iops_in_progress'),
            'merged_reads': fields.get('merged_reads'),
            'merged_writes': fields.get('merged_writes'),
            'read_bytes': fields.get('read_bytes'),
            'read_time': fields.get('read_time'),
            'reads': fields.get('reads'),
            'weighted_io_time': fields.get('weighted_io_time'),
            'write_bytes': fields.get('write_bytes'),
            'write_time': fields.get('write_time'),
            'writes': fields.get('writes')
        }
        
        writer.writerow(row)

print("CSV conversion complete.")
