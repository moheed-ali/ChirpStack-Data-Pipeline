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

# Function to convert JSON data to pro CSV
def json_to_csv_pro(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['timestamp', 'blocked', 'dead', 'idle', 
                                                     'paging', 'running', 'sleeping', 
                                                     'stopped', 'total', 'total_threads', 
                                                     'unknown', 'zombies'])
        writer.writeheader()

        for line in infile:
            data = json.loads(line)
            fields = data.get('fields', {})

            row = {
                'timestamp': data.get('timestamp', None),
                'blocked': fields.get('blocked', None),
                'dead': fields.get('dead', None),
                'idle': fields.get('idle', None),
                'paging': fields.get('paging', None),
                'running': fields.get('running', None),
                'sleeping': fields.get('sleeping', None),
                'stopped': fields.get('stopped', None),
                'total': fields.get('total', None),
                'total_threads': fields.get('total_threads', None),
                'unknown': fields.get('unknown', None),
                'zombies': fields.get('zombies', None)
            }

            writer.writerow(row)

# Function to convert JSON data to net CSV
def json_to_csv_net(input_file, output_file):
    with open(input_file, 'r') as in_file, open(output_file, 'w', newline='') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=['timestamp', 'bytes_recv', 'bytes_sent', 'drop_in', 
                                                      'drop_out', 'err_in', 'err_out', 'packets_recv', 
                                                      'packets_sent', 'speed', 'icmp_inaddrmaskreps', 
                                                      'icmp_inaddrmasks', 'icmp_incsumerrors', 
                                                      'icmp_indestunreachs', 'icmp_inechoreps', 
                                                      'icmp_inechos', 'icmp_inerrors', 'icmp_inmsgs', 
                                                      'icmp_inparmprobs', 'icmp_inredirects', 
                                                      'icmp_insrcquenchs', 'icmp_intimeexcds', 
                                                      'icmp_intimestampreps', 'icmp_intimestamps', 
                                                      'icmp_outaddrmaskreps', 'icmp_outaddrmasks', 
                                                      'icmp_outdestunreachs', 'icmp_outechoreps', 
                                                      'icmp_outechos', 'icmp_outerrors', 'icmp_outmsgs', 
                                                      'icmp_outparmprobs', 'icmp_outratelimitglobal', 
                                                      'icmp_outratelimithost', 'icmp_outredirects', 
                                                      'icmp_outsrcquenchs', 'icmp_outtimeexcds', 
                                                      'icmp_outtimestampreps', 'icmp_outtimestamps', 
                                                      'ip_defaultttl', 'ip_forwarding', 'ip_forwdatagrams', 
                                                      'ip_fragcreates', 'ip_fragfails', 'ip_fragoks', 
                                                      'ip_inaddrerrors', 'ip_indelivers', 'ip_indiscards', 
                                                      'ip_inhdrerrors', 'ip_inreceives', 'ip_inunknownprotos', 
                                                      'ip_outdiscards', 'ip_outnoroutes', 'ip_outrequests', 
                                                      'ip_reasmfails', 'ip_reasmoks', 'ip_reasmreqds', 
                                                      'ip_reasmtimeout', 'tcp_activeopens', 'tcp_attemptfails', 
                                                      'tcp_currestab', 'tcp_estabresets', 'tcp_incsumerrors', 
                                                      'tcp_inerrs', 'tcp_insegs', 'tcp_maxconn', 'tcp_outrsts', 
                                                      'tcp_outsegs', 'tcp_passiveopens', 'tcp_retranssegs', 
                                                      'tcp_rtoalgorithm', 'tcp_rtomax', 'tcp_rtomin', 
                                                      'udp_ignoredmulti', 'udp_incsumerrors', 'udp_indatagrams', 
                                                      'udp_inerrors', 'udp_memerrors', 'udp_noports', 
                                                      'udp_outdatagrams', 'udp_rcvbuferrors', 'udp_sndbuferrors', 
                                                      'udplite_ignoredmulti', 'udplite_incsumerrors', 
                                                      'udplite_indatagrams', 'udplite_inerrors', 
                                                      'udplite_memerrors', 'udplite_noports', 
                                                      'udplite_outdatagrams', 'udplite_rcvbuferrors', 
                                                      'udplite_sndbuferrors'])
        writer.writeheader()
        
        for line in in_file:
            data = json.loads(line)
            flattened_data = flatten_json(data['fields'])
            row = {'timestamp': data['timestamp']}
            for key in writer.fieldnames[1:]:
                row[key] = flattened_data.get(key, 'null')
            writer.writerow(row)

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




# Main function to execute the conversions
def main(input_file):
    json_to_csv_cpu(input_file, 'CSV/cpu.csv')
    json_to_csv_disk(input_file, 'CSV/disk.csv')
    json_to_csv_diskio(input_file, 'CSV/diskio.csv')
    json_to_csv_mem(input_file, 'CSV/mem.csv')
    json_to_csv_net(input_file, 'CSV/net.csv')
    json_to_csv_pro(input_file, 'CSV/pro.csv')
    print("CSV conversion complete.")

# Usage
if __name__ == "__main__":
    # input_file = input("Enter the input file path: ")
    input_file = "metrics.out"
    main(input_file)
