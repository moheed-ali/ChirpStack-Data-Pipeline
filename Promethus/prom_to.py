import requests
from datetime import datetime, timedelta
import csv
import schedule
import time

# ANSI escape code for blue text
BLUE = "\033[94m"
RESET = "\033[0m"

url = 'http://localhost:9090/api/v1/query'
query_list = ['up',
            'uplink_count_total',
            'api_requests_handled_seconds_bucket',
            'api_requests_handled_seconds_count',
            'api_requests_handled_seconds_sum',
            'api_requests_handled_total',
            'backend_semtechdup_gateway_ack_rate',
            'backend_semtechudp_gateway_ack_rate_count',
            'backend_semtechudp_gateway_connect_count',
            'backend_semtechudp_gateway_diconnect_count',
            'backend_semtechudp_udp_received_count',
            'backend_semtechudp_udp_sent_count',
            'deduplicate_locked_count_total',
            'deduplicate_no_lock_count_total',
            'gateway_backend_mqtt_commands_total',
            'gateway_backend_mqtt_events_total',
            'go_gc_duration_seconds',
            'go_gc_duration_seconds_count',
            'go_gc_duration_seconds_sum',
            'go_goroutines',
            'go_info',
            'go_memstats_alloc_bytes',
            'go_memstats_alloc_bytes_total',
            'go_memstats_buck_hash_sys_bytes',
            'go_memstats_frees_total',
            'go_memstats_gc_sys_bytes',
            'go_memstats_heap_alloc_bytes',
            'go_memstats_heap_idle_bytes',
            'go_memstats_heap_inuse_bytes',
            'go_memstats_heap_objects',
            'go_memstats_heap_released_bytes',
            'go_memstats_heap_sys_bytes',
            'go_memstats_last_gc_time_seconds',
            'go_memstats_lookups_total',
            'go_memstats_mallocs_total',
            'go_memstats_mcache_inuse_bytes', 
            'go_memstats_mcache_sys_bytes',
            'go_memstats_mspan_inuse_bytes',
            'go_memstats_mspan_sys_bytes',
            'go_memstats_next_gc_bytes',
            'go_memstats_other_sys_bytes',
            'go_memstats_stack_inuse_bytes',
            'go_memstats_stack_sys_bytes',
            'go_memstats_sys_bytes',
            'go_threads',
            'integration_mqtt_command_count',
            'integration_mqtt_connect_count',
            'integration_mqtt_disconnect_count',
            'integration_mqtt_event_count',
            'integration_mqtt_reconnect_count',
            'integration_mqtt_state_count',
            'process_cpu_seconds_total',
            'process_max_fds',
            'process_open_fds',
            'process_resident_memory_bytes',
            'process_start_time_seconds',
            'process_virtual_memory_bytes',
            'process_virtual_memory_max_bytes',
            'promhttp_metric_handler_requests_in_flight',
            'promhttp_metric_handler_requests_total',
            'scrape_duration_seconds',
            'scrape_samples_post_metric_relabeling',
            'scrape_samples_scraped',
            'scrape_series_added',
            'storage_pg_conn_get_duration_seconds_bucket',
            'storage_pg_conn_get_duration_seconds_count',
            'storage_pg_conn_get_duration_seconds_sum',
            'storage_redis_conn_get_duration_seconds_bucket',
            'storage_redis_conn_get_duration_seconds_count',
            'storage_redis_conn_get_duration_seconds_sum'
            ]

def fetch_and_save_data():
    current_time = datetime.now()

    print(BLUE + "Current time: ", current_time, RESET)

    # Subtract two hours
    current_time = current_time - timedelta(hours=2)
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    for query in query_list:
        params = {'time': formatted_time, 'query': query}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                print(BLUE + f"Query '{query}' returned data." + RESET)
                result_data = data["data"]["result"]
                
                filename = "/home/eleve/ChirpStack-Data-Pipeline/OUTPUT/prom_data.csv"
                with open(filename, mode='a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=["Timestamp", "Event", "Instance", "Job", "Query", "Value"])
                    if file.tell() == 0:
                        writer.writeheader()
                    for result in result_data:
                        writer.writerow({
                            "Timestamp": result["value"][0],
                            "Query": query,
                            "Event": result["metric"].get("event", None),
                            "Instance": result["metric"].get("instance", None),
                            "Job": result["metric"].get("job", None),
                            "Value": result["value"][1]
                        })
                
                print(BLUE + f"Data has been written to {filename}" + RESET)        
            else:
                print(f"Query '{query}' did not return any data.")
        else:
            print(f"Request for query '{query}' failed with status code {response.status_code}")

# Schedule the job to run every 10 seconds
schedule.every(0.5).seconds.do(fetch_and_save_data)

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(0.01)  # Adjust the sleep time as needed for accuracy

