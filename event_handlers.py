from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from chirpstack_api import integration
from google.protobuf.json_format import Parse
import csv
import time
import subprocess
import sys

docker_images = ["5d3a2f93eb20", "0e734c94da99", "f9e5c766cf94", "a64000d6807e"] 


class ChirpStackHandler(BaseHTTPRequestHandler):
    json = True
    csv_filename = "up_data.csv"

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        query_args = parse_qs(urlparse(self.path).query)

        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len)

        event_type = query_args.get("event", [""])[0]

        if event_type == "up":
            self.handle_uplink(body)
        if event_type == "down":
            self.handle_downlink(body)    
        elif event_type == "join":
            self.handle_join(body)
        else:
            # print("No");
            print(f"Handler for event {event_type} is not implemented")

    def handle_downlink(self, body):
        down = self.unmarshal(body, integration.DownlinkEvent())
        print("Downlink received for device: %s with payload: %s" % (down.device_info.dev_eui, down.data.hex()))    

    def handle_uplink(self, body):
        """
        Handles the ChirpStack uplink event.
        Extracts information from the uplink event and writes it to a CSV file, considering multiple gateways.

        Parameters:
            body (bytes): The raw request body containing the ChirpStack UplinkEvent.

        Logic:
            - Unmarshals the ChirpStack UplinkEvent from the JSON body.
            - Extracts common data for all gateways.
            - Checks if the CSV file exists and writes headers if not.
            - Iterates through each gateway's rxInfo, copies common data, and appends gateway-specific information.
            - Extracts txInfo values (common for all gateways) and appends them to the row data.
            - Writes the row data to the CSV file.

        Note:
            This logic ensures that a new row is created for each gateway's information, while common data for the
            uplink event is consistent across all rows.
        """
        
        up = self.unmarshal(body, integration.UplinkEvent())
        print(f"Uplink received from: {up.device_info.device_name} with F count: {up.f_cnt}")

        # Extract values from the 'up' object (common for all gateways)
        common_data = [
            self.get_timestamp(),
            up.deduplication_id,
            up.time.seconds,
            up.device_info.tenant_id,
            up.device_info.tenant_name,
            up.device_info.application_id,
            up.device_info.application_name,
            up.device_info.device_profile_id,
            up.device_info.device_profile_name,
            up.device_info.device_name,
            up.device_info.dev_eui,
            up.dev_addr,
            up.dr,
            up.f_port,
            up.data.hex(),
            up.f_cnt
        ]

        # Check if the CSV file exists and write headers if not
        if not self.does_csv_exist():
            self.write_csv_headers()

        # Open the CSV file in append mode and write the common data
        with open(self.csv_filename, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Extract rxInfo values for each gateway
            for rx_info in up.rx_info:
                row_data = common_data.copy()

                rx_info_values = [
                    rx_info.gateway_id,
                    rx_info.uplink_id,
                    rx_info.rssi,
                    rx_info.snr,
                    rx_info.context
                ]

                row_data.extend(rx_info_values)

                # Extract txInfo values (common for all gateways)
                if up.HasField('tx_info'):
                    tx_info = up.tx_info
                    tx_info_values = [
                        tx_info.frequency,
                        tx_info.modulation.lora.bandwidth,
                        tx_info.modulation.lora.spreading_factor,
                        tx_info.modulation.lora.code_rate
                    ]
                    row_data.extend(tx_info_values)
                else:
                    row_data.extend(["", "", "", ""])

                docker_stats = self.get_docker_stats(docker_images)
                
                for stat in docker_stats:
                    row_data.extend(stat)
                
                # Write the row data to the CSV file
                csv_writer.writerow(row_data)

    def handle_join(self, body):
        join = self.unmarshal(body, integration.JoinEvent())
        print(f"Device: {join.device_info.dev_eui} joined with DevAddr: {join.dev_addr}")

    def unmarshal(self, body, pl):
        if self.json:
            return Parse(body, pl)

        pl.ParseFromString(body)
        return pl

    def does_csv_exist(self):
        try:
            with open(self.csv_filename, 'r'):
                return True
        except FileNotFoundError:
            return False

    def write_csv_headers(self):
        header_row = [
            "Timestamp",
            "Deduplication ID",
            "Time Seconds",
            "Tenant ID",
            "Tenant Name",
            "Application ID",
            "Application Name",
            "Device Profile ID",
            "Device Profile Name",
            "Device Name",
            "Dev EUI",
            "Dev Addr",
            "Dr",
            "fPort",
            "Data Hex",
            "F Count",
            "rxInfo Gateway ID",
            "rxInfo Uplink ID",
            "rxInfo RSSI",
            "rxInfo SNR",
            "rxInfo Context",
            "txInfo Frequency",
            "Modulation-lora txInfo Bandwidth",
            "Modulation-lora Spreading Factor",
            "Modulation-lora Code Rate",
            "Container",
            "Name",
            "CPUPerc",
            "MemUsage",
            "NetIO",
            "BlockIO",
            "PIDs",
            "Container",
             "Name",
            "CPUPerc",
            "MemUsage",
            "NetIO",
            "BlockIO",
            "PIDs",
            "Container",
            "Name",
            "CPUPerc",
            "MemUsage",
            "NetIO",
            "BlockIO",
            "PIDs",
            "Container",
            "Name",
            "CPUPerc",
            "MemUsage",
            "NetIO",
            "BlockIO",
            "PIDs"       
        ]

        with open(self.csv_filename, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header_row)

    def get_timestamp(self):
        return int(time.time())
    
    def get_docker_stats(self, container_names):
        try:
            # Run the docker stats command for multiple containers
            result = subprocess.run(
                ['docker', 'stats', '--no-stream', '--format', '{{.Container}},{{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.NetIO}},{{.BlockIO}},{{.PIDs}}'] + container_names,
                capture_output=True, text=True
            )

            # Check if the command was successful
            if result.returncode == 0:
                # Split the output into lines and filter out empty lines
                stats = [line.split(',') for line in result.stdout.split('\n') if line.strip()]
                return stats
            else:
                return [f'Error running docker stats command for containers {", ".join(container_names)}']
        except Exception as e:
            return [f'Error: {str(e)}']
