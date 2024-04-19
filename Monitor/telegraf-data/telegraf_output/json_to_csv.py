import json
import csv

# Function to handle missing keys by returning None
def get_field(obj, key):
    return obj.get(key, None)

# Function to convert JSON data to CPU CSV
def json_to_csv_cpu(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        
        # Write the header row
        writer.writerow(["timestamp", "cpu", "usage_guest", "usage_guest_nice", "usage_idle", 
                         "usage_iowait", "usage_irq", "usage_nice", "usage_softirq", 
                         "usage_steal", "usage_system", "usage_user"])
        
        for line in infile:
            data = json.loads(line)
            timestamp = data.get('timestamp', None)
            tags = data.get('tags', {})
            fields = data.get('fields', {})
            cpu = tags.get('cpu', None)
            
            writer.writerow([
                timestamp,
                cpu,
                fields.get('usage_guest', None),
                fields.get('usage_guest_nice', None),
                fields.get('usage_idle', None),
                fields.get('usage_iowait', None),
                fields.get('usage_irq', None),
                fields.get('usage_nice', None),
                fields.get('usage_softirq', None),
                fields.get('usage_steal', None),
                fields.get('usage_system', None),
                fields.get('usage_user', None)
            ])

# Function to convert JSON data to Disk CSV
def json_to_csv_disk(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        
        # Write the header row
        writer.writerow(['timestamp', 'free', 'inodes_free', 'inodes_total', 'inodes_used', 'inodes_used_percent', 'total', 'used', 'used_percent', 'name', 'device', 'fstype', 'host', 'mode', 'path'])
        
        for line in infile:
            data = json.loads(line)
            timestamp = data.get('timestamp', None)
            fields = data.get('fields', {})
            tags = data.get('tags', {})
            
            writer.writerow([
                timestamp,
                fields.get('free', None),
                fields.get('inodes_free', None),
                fields.get('inodes_total', None),
                fields.get('inodes_used', None),
                fields.get('inodes_used_percent', None),
                fields.get('total', None),
                fields.get('used', None),
                fields.get('used_percent', None),
                data.get('name', None),
                tags.get('device', None),
                tags.get('fstype', None),
                tags.get('host', None),
                tags.get('mode', None),
                tags.get('path', None)
            ])

# Function to convert JSON data to Disk IO CSV
def json_to_csv_diskio(input_file, output_file):
    with open(input_file, 'r') as in_file, open(output_file, 'w', newline='') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=['timestamp', 'name', 'host', 'wwid', 'io_time', 'iops_in_progress', 'merged_reads', 'merged_writes', 'read_bytes', 'read_time', 'reads', 'weighted_io_time', 'write_bytes', 'write_time', 'writes'])
        writer.writeheader()
        
        for line in in_file:
            data = json.loads(line)
            fields = data.get('fields', {})
            tags = data.get('tags', {})
            
            row = {
                'timestamp': data.get('timestamp', None),
                'name': data.get('name', None),
                'host': tags.get('host', None),
                'wwid': tags.get('wwid', None),
                'io_time': fields.get('io_time', None),
                'iops_in_progress': fields.get('iops_in_progress', None),
                'merged_reads': fields.get('merged_reads', None),
                'merged_writes': fields.get('merged_writes', None),
                'read_bytes': fields.get('read_bytes', None),
                'read_time': fields.get('read_time', None),
                'reads': fields.get('reads', None),
                'weighted_io_time': fields.get('weighted_io_time', None),
                'write_bytes': fields.get('write_bytes', None),
                'write_time': fields.get('write_time', None),
                'writes': fields.get('writes', None)
            }
            
            writer.writerow(row)


# Main function to execute the conversions
def main(input_file):
    json_to_csv_cpu(input_file, 'CSV/cpu.csv')
    json_to_csv_disk(input_file, 'CSV/disk.csv')
    json_to_csv_diskio(input_file, 'CSV/diskio.csv')
    print("CSV conversion complete.")

# Usage
if __name__ == "__main__":
    # input_file = input("Enter the input file path: ")
    input_file = "metrics.out"
    main(input_file)
