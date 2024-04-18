from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from chirpstack_api import integration
from google.protobuf.json_format import Parse
import csv
import time
import subprocess
import sys

# docker_images = ["5d3a2f93eb20", "0e734c94da99", "f9e5c766cf94", "a64000d6807e"] 


class ChirpStackHandler(BaseHTTPRequestHandler):
    json = True
    csv_filename = "up_data.csv"
    csv_filename0 = "ack_data.csv"
    csv_filename1 = "join_data.csv"
    csv_filename2 = "log_data.csv"
    csv_filename3 = "status_data.csv"
    csv_filename4 = "txack_data.csv"
    csv_filename5 = "location_data.csv"
    csv_filename6 = "integration_data.csv"

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        query_args = parse_qs(urlparse(self.path).query)

        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len)

        event_type = query_args.get("event", [""])[0]

        if event_type == "up":
            self.handle_uplink(body)
        elif event_type == "location":
            self.handle_location(body)    
        elif event_type == "join":
            self.handle_join(body)
        elif event_type == "log":
            self.handle_log(body)
        elif event_type == "ack":
            self.handle_ack(body)
        elif event_type == "status":
            self.handle_status(body)
        elif event_type == "txack":
            self.handle_txack(body)
        elif event_type == "integration":
            self.handle_integration(body)
        else:
            # print("No");
            print(f"Handler for event {event_type} is not implemented")

    def handle_location(self, body):
        loc = self.unmarshal(body, integration.LocationEvent())
        print("Location received for device: %s with Application Name: %s" % (loc.device_info.dev_eui, loc.device_info.application_name))    

        loc_row_data = [
            loc.deduplication_id,
            loc.time.seconds,
            loc.device_info.tenant_id,
            loc.device_info.tenant_name,
            loc.device_info.application_id,
            loc.device_info.application_name,
            loc.device_info.device_profile_id,
            loc.device_info.device_profile_name,
            loc.device_info.device_name,
            loc.device_info.dev_eui,
            loc.location.latitude,
            loc.location.longitude,
            loc.location.altitude
        ]

        if not self.does_loc_csv_exist():
            self.write_loc_csv_headers()   

        # Open the CSV file in append mode and write the common data
        with open(self.csv_filename5, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the row data to the CSV file
            csv_writer.writerow(loc_row_data) 

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
        if not self.does_up_csv_exist():
            self.write_up_csv_headers()

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

                # docker_stats = self.get_docker_stats(docker_images)
                
                # for stat in docker_stats:
                #     row_data.extend(stat)
                
                # Write the row data to the CSV file
                csv_writer.writerow(row_data)

    def handle_ack(self, body):
        ack = self.unmarshal(body, integration.AckEvent())
        print("Ack received for device: %s with fCntDown: %s" % (ack.device_info.dev_eui, ack.f_cnt_down))   

        ack_row_data = [
            ack.deduplication_id,
            ack.time.seconds,
            ack.device_info.tenant_id,
            ack.device_info.tenant_name,
            ack.device_info.application_id,
            ack.device_info.application_name,
            ack.device_info.device_profile_id,
            ack.device_info.device_profile_name,
            ack.device_info.device_name,
            ack.device_info.dev_eui,
            ack.queue_item_id,
            ack.acknowledged,
            ack.f_cnt_down
        ] 

        if not self.does_ack_csv_exist():
            self.write_ack_csv_headers()   

        # Open the CSV file in append mode and write the common data
        with open(self.csv_filename0, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the row data to the CSV file
            csv_writer.writerow(ack_row_data) 

    def handle_join(self, body):
        join = self.unmarshal(body, integration.JoinEvent())
        print(f"Device: {join.device_info.dev_eui} joined with DevAddr: {join.dev_addr}")

        join_row_data = [
            join.deduplication_id,
            join.time.seconds,
            join.device_info.tenant_id,
            join.device_info.tenant_name,
            join.device_info.application_id,
            join.device_info.application_name,
            join.device_info.device_profile_id,
            join.device_info.device_profile_name,
            join.device_info.device_name,
            join.device_info.dev_eui,
            join.devAddr
        ]

        # Check if the CSV file exists and write headers if not
        if not self.does_join_csv_exist():
            self.write_join_csv_headers()
        
        with open(self.csv_filename1, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the row data to the CSV file
            csv_writer.writerow(join_row_data)

    def handle_log(self, body):
        log = self.unmarshal(body, integration.LogEvent())
        print("Device: %s Logged with Dev. Name: %s" % (log.device_info.dev_eui, log.device_info.device_name))
        
        
        log_row_data = [
            log.time.seconds,
            log.device_info.tenant_id,
            log.device_info.tenant_name,
            log.device_info.application_id,
            log.device_info.application_name,
            log.device_info.device_profile_id,
            log.device_info.device_profile_name,
            log.device_info.device_name,
            log.device_info.dev_eui,
            log.level,
            log.code,
            log.description,
            log.context["deduplication_id"]
            
        ]

        # Check if the CSV file exists and write headers if not
        if not self.does_log_csv_exist():
            self.write_log_csv_headers()
        
        # Open the CSV file in append mode and write the common data
        with open(self.csv_filename2, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the row data to the CSV file
            csv_writer.writerow(log_row_data)

    def handle_status(self, body):
        status = self.unmarshal(body, integration.StatusEvent())
        print("Status received for device: %s with battery Level: %s" % (status.device_info.dev_eui, status.battery_level))   

        ack_row_data = [
            status.deduplication_id,
            status.time.seconds,
            status.device_info.tenant_id,
            status.device_info.tenant_name,
            status.device_info.application_id,
            status.device_info.application_name,
            status.device_info.device_profile_id,
            status.device_info.device_profile_name,
            status.device_info.device_name,
            status.device_info.dev_eui,
            status.margin,
            status.external_power_source,
            status.battery_level_unavailable,
            status.battery_level
        ] 

        if not self.does_status_csv_exist():
            self.write_ack_status_headers()   

        # Open the CSV file in append mode and write the common data
        with open(self.csv_filename3, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the row data to the CSV file
            csv_writer.writerow(ack_row_data) 

    def handle_txack(self, body):
        txack = self.unmarshal(body, integration.TxAckEvent())
        print(f"txack received from: {txack.device_info.device_name} with F count: {up.f_cnt}")

        # Extract values from the 'up' object (common for all gateways)
        common_data = [
            txack.downlink_id,
            txack.time.seconds,
            txack.device_info.tenant_id,
            txack.device_info.tenant_name,
            txack.device_info.application_id,
            txack.device_info.application_name,
            txack.device_info.device_profile_id,
            txack.device_info.device_profile_name,
            txack.device_info.device_name,
            txack.device_info.dev_eui,
            txack.queue_item_id,
            txack.f_cnt_down,
            txack.gateway_id
        ]

        # Check if the CSV file exists and write headers if not
        if not self.does_txack_csv_exist():
            self.write_txack_csv_headers()

        # Open the CSV file in append mode and write the common data
        with open(self.csv_filename4, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Extract rxInfo values for each gateway
            for tx_info in txack.rx_info:
                row_data = common_data.copy()

                tx_info_values = [
                    tx_info.frequency,
                    tx_info.power,
                    tx_info.modulation.lora.bandwidth,
                    tx_info.modulation.lora.spreading_factor,
                    tx_info.modulation.lora.code_rate,
                    tx_info.modulation.lora.polarization_inversion,
                    tx_info.timng.delay.delay,
                    tx_info.context
                ]

                row_data.extend(tx_info_values)

                csv_writer.writerow(row_data)

    def handle_integration(self, body):
        inte = self.unmarshal(body, integration.IntegrationEvent())
        print(f"Integration received from: {inte.device_info.device_name} with F count: {inte.f_cnt}")

        # Extract values from the 'up' object (common for all gateways)
        inte_data = [
            inte.deduplication_id,
            inte.time.seconds,
            inte.device_info.tenant_id,
            inte.device_info.tenant_name,
            inte.device_info.application_id,
            inte.device_info.application_name,
            inte.device_info.device_profile_id,
            inte.device_info.device_profile_name,
            inte.device_info.device_name,
            inte.device_info.dev_eui,
            inte.integration_name,
            inte.event_type,
            inte.object
        ]

        if not self.does_inte_csv_exist():
            self.write_inte_status_headers()   

        # Open the CSV file in append mode and write the common data
        with open(self.csv_filename6, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the row data to the CSV file
            csv_writer.writerow(inte_data)         

    def unmarshal(self, body, pl):
        if self.json:
            return Parse(body, pl)

        pl.ParseFromString(body)
        return pl

    def does_up_csv_exist(self):
        try:
            with open(self.csv_filename, 'r'):
                return True
        except FileNotFoundError:
            return False

    def does_log_csv_exist(self):
        try:
            with open(self.csv_filename2, 'r'):
                return True
        except FileNotFoundError:
            return False
        
    def does_join_csv_exist(self):
        try:
            with open(self.csv_filename1, 'r'):
                return True
        except FileNotFoundError:
            return False
    
    def does_ack_csv_exist(self):
        try:
            with open(self.csv_filename0, 'r'):
                return True
        except FileNotFoundError:
            return False
        
    def does_status_csv_exist(self):
        try:
            with open(self.csv_filename3, 'r'):
                return True
        except FileNotFoundError:
            return False
        
    def does_loc_csv_exist(self):
        try:
            with open(self.csv_filename5, 'r'):
                return True
        except FileNotFoundError:
            return False
    
    def does_txack_csv_exist(self):
        try:
            with open(self.csv_filename4, 'r'):
                return True
        except FileNotFoundError:
            return False
        
    def does_inte_csv_exist(self):
        try:
            with open(self.csv_filename6, 'r'):
                return True
        except FileNotFoundError:
            return False

    def write_up_csv_headers(self):
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
            "Modulation-lora Code Rate"      
        ]

        with open(self.csv_filename, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header_row)

    def write_txack_csv_headers(self):
        header_row = [
            "Downlink ID",
            "Time Seconds",
            "Tenant ID",
            "Tenant Name",
            "Application ID",
            "Application Name",
            "Device Profile ID",
            "Device Profile Name",
            "Device Name",
            "Dev EUI",
            "Queue Item Id",
            "fCnt Down",
            "Gateway Id",
            "txInfo Frequency",
            "txInfo Power",
            "Modulation-lora txInfo Bandwidth",
            "Modulation-lora Spreading Factor",
            "Modulation-lora Code Rate" 
            "Modulation-lora Polarization Inversion",
            "Timing-Delay",
            "Context"
        ]

        with open(self.csv_filename4, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header_row)

    def write_inte_csv_headers(self):
        header_row = [
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
            "Integration Name",
            "Event Type",
            "Object"
        ]

        with open(self.csv_filename6, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header_row)

    def write_log_csv_headers(self):
        header_row = [
            "Time Seconds",
            "Tenant ID",
            "Tenant Name",
            "Application ID",
            "Application Name",
            "Device Profile ID",
            "Device Profile Name",
            "Device Name",
            "Dev EUI",
            "Log Level",
            "Log Code", 
            "Log Description",
            "Log Context"      
        ]

        with open(self.csv_filename2, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header_row)
    
    def write_join_csv_headers(self):
        header_row = [
            "Deduplication Id",
            "Time Seconds",
            "Tenant ID",
            "Tenant Name",
            "Application ID",
            "Application Name",
            "Device Profile ID",
            "Device Profile Name",
            "Device Name",
            "Dev EUI",
            "Dev Addr"     
        ]

        with open(self.csv_filename1, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header_row)
    
    def write_ack_csv_headers(self):
        header_row = [
            "Deduplication Id",
            "Time Seconds",
            "Tenant ID",
            "Tenant Name",
            "Application ID",
            "Application Name",
            "Device Profile ID",
            "Device Profile Name",
            "Device Name",
            "Dev EUI",
            "queueItemId",
            "acknowledged",
            "fCntDown"     
        ]

        with open(self.csv_filename0, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header_row)

    def write_loc_csv_headers(self):
        header_row = [
            "Deduplication Id",
            "Time Seconds",
            "Tenant ID",
            "Tenant Name",
            "Application ID",
            "Application Name",
            "Device Profile ID",
            "Device Profile Name",
            "Device Name",
            "Dev EUI",
            "location latitude",
            "location longitude",
            "location altitude"     
        ]

        with open(self.csv_filename5, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header_row)
    
    def write_status_csv_headers(self):
        header_row = [
            "Deduplication Id",
            "Time Seconds",
            "Tenant ID",
            "Tenant Name",
            "Application ID",
            "Application Name",
            "Device Profile ID",
            "Device Profile Name",
            "Device Name",
            "Dev EUI",
            "Magin",
            "External Power Source",
            "Battery Level Unavailable",
            "Battery Level"     
        ]

        with open(self.csv_filename3, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header_row)

    def get_timestamp(self):
        return int(time.time())
    
    # def get_docker_stats(self, container_names):
    #     try:
    #         # Run the docker stats command for multiple containers
    #         result = subprocess.run(
    #             ['docker', 'stats', '--no-stream', '--format', '{{.Container}},{{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.NetIO}},{{.BlockIO}},{{.PIDs}}'] + container_names,
    #             capture_output=True, text=True
    #         )

    #         # Check if the command was successful
    #         if result.returncode == 0:
    #             # Split the output into lines and filter out empty lines
    #             stats = [line.split(',') for line in result.stdout.split('\n') if line.strip()]
    #             return stats
    #         else:
    #             return [f'Error running docker stats command for containers {", ".join(container_names)}']
    #     except Exception as e:
    #         return [f'Error: {str(e)}']
