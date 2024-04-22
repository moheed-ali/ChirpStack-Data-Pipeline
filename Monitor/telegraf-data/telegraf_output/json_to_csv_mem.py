import json
import csv

# Read data from data.out file
with open('metrics.out', 'r') as f:
    data = f.readlines()

# Define CSV header
csv_header = [
    "timestamp",
    "active",
    "available",
    "available_percent",
    "buffered",
    "cached",
    "commit_limit",
    "committed_as",
    "dirty",
    "free",
    "high_free",
    "high_total",
    "huge_page_size",
    "huge_pages_free",
    "huge_pages_total",
    "inactive",
    "low_free",
    "low_total",
    "mapped",
    "page_tables",
    "shared",
    "slab",
    "sreclaimable",
    "sunreclaim",
    "swap_cached",
    "swap_free",
    "swap_total",
    "total",
    "used",
    "used_percent",
    "vmalloc_chunk",
    "vmalloc_total",
    "vmalloc_used",
    "write_back",
    "write_back_tmp",
    "name",
    "tags_host"
]

# Write data to CSV file
with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_header)

    for line in data:
        # Parse JSON
        json_data = json.loads(line)

        # Extract timestamp
        timestamp = json_data['timestamp']

        # Extract fields
        fields = json_data.get('fields', {})
        name = json_data.get('name', '')
        tags_host = json_data['tags'].get('host', '')

        # Create row for CSV
        row = [timestamp]
        for header in csv_header[1:-2]:  # Exclude 'timestamp', 'name', and 'tags_host'
            value = fields.get(header, 'null')
            row.append(value)
        row.extend([name, tags_host])

        # Write row to CSV file
        writer.writerow(row)

print("CSV file has been created successfully.")
