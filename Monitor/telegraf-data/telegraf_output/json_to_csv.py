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
        writer.writerow(['timestamp', 'free', 'inodes_free', 'inodes_total', 'inodes_used', 
                         'inodes_used_percent', 'total', 'used', 'used_percent', 'name', 'device', 
                         'fstype', 'host', 'mode', 'path'])
        
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
        writer = csv.DictWriter(out_file, fieldnames=['timestamp', 'name', 'host', 'wwid', 
                                                      'io_time', 'iops_in_progress', 'merged_reads', 
                                                      'merged_writes', 'read_bytes', 'read_time', 
                                                      'reads', 'weighted_io_time', 'write_bytes', 
                                                      'write_time', 'writes'])
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

# Function to convert JSON data to MEM CSV
def json_to_csv_mem(input_file, output_file):
    with open(input_file, 'r') as in_file, open(output_file, 'w', newline='') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=['timestamp', 'name', 'tags_host', 'active', 
                                                      'available', 'available_percent', 'buffered', 
                                                      'cached', 'commit_limit', 'committed_as', 
                                                      'dirty', 'free', 'high_free', 'high_total', 
                                                      'huge_page_size', 'huge_pages_free', 
                                                      'huge_pages_total', 'inactive', 'low_free', 
                                                      'low_total', 'mapped', 'page_tables', 'shared', 
                                                      'slab', 'sreclaimable', 'sunreclaim', 'swap_cached', 
                                                      'swap_free', 'swap_total', 'total', 'used', 
                                                      'used_percent', 'vmalloc_chunk', 'vmalloc_total', 
                                                      'vmalloc_used', 'write_back', 'write_back_tmp'])
        writer.writeheader()
        
        for line in in_file:
            # Parse JSON
            json_data = json.loads(line)

            # Extract timestamp
            timestamp = json_data.get('timestamp', None)

            # Extract fields
            fields = json_data.get('fields', {})
            name = json_data.get('name', '')
            tags_host = json_data.get('tags', {}).get('host', '')

            # Create row for CSV
            row = {
                'timestamp': timestamp,
                'name': name,
                'tags_host': tags_host,
                'active': fields.get('active', None),
                'available': fields.get('available', None),
                'available_percent': fields.get('available_percent', None),
                'buffered': fields.get('buffered', None),
                'cached': fields.get('cached', None),
                'commit_limit': fields.get('commit_limit', None),
                'committed_as': fields.get('committed_as', None),
                'dirty': fields.get('dirty', None),
                'free': fields.get('free', None),
                'high_free': fields.get('high_free', None),
                'high_total': fields.get('high_total', None),
                'huge_page_size': fields.get('huge_page_size', None),
                'huge_pages_free': fields.get('huge_pages_free', None),
                'huge_pages_total': fields.get('huge_pages_total', None),
                'inactive': fields.get('inactive', None),
                'low_free': fields.get('low_free', None),
                'low_total': fields.get('low_total', None),
                'mapped': fields.get('mapped', None),
                'page_tables': fields.get('page_tables', None),
                'shared': fields.get('shared', None),
                'slab': fields.get('slab', None),
                'sreclaimable': fields.get('sreclaimable', None),
                'sunreclaim': fields.get('sunreclaim', None),
                'swap_cached': fields.get('swap_cached', None),
                'swap_free': fields.get('swap_free', None),
                'swap_total': fields.get('swap_total', None),
                'total': fields.get('total', None),
                'used': fields.get('used', None),
                'used_percent': fields.get('used_percent', None),
                'vmalloc_chunk': fields.get('vmalloc_chunk', None),
                'vmalloc_total': fields.get('vmalloc_total', None),
                'vmalloc_used': fields.get('vmalloc_used', None),
                'write_back': fields.get('write_back', None),
                'write_back_tmp': fields.get('write_back_tmp', None),
            }

            # Write row to CSV file
            writer.writerow(row)



# Main function to execute the conversions
def main(input_file):
    json_to_csv_cpu(input_file, 'CSV/cpu.csv')
    json_to_csv_disk(input_file, 'CSV/disk.csv')
    json_to_csv_diskio(input_file, 'CSV/diskio.csv')
    json_to_csv_mem(input_file, 'CSV/mem.csv')
    print("CSV conversion complete.")

# Usage
if __name__ == "__main__":
    # input_file = input("Enter the input file path: ")
    input_file = "metrics.out"
    main(input_file)
