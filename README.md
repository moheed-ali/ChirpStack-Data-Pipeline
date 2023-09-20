# How to Run the Python Code for InfluxDB Data Ingestion & Grafana Integration
This README guide will walk you through the process of running the provided Python code to ingest data into InfluxDB using the ChirpStack API. The code listens for incoming ChirpStack events (uplinks and joins), processes the data, and stores it in InfluxDB. Here are the steps to run the code:

## Prerequisites

Before you begin, ensure you have the following prerequisites:

- **Python Installed**: You need to have Python installed on your system. You can download Python from the [official website](https://www.python.org/downloads/).

- **InfluxDB and ChirpStack Setup**: Make sure you have InfluxDB and ChirpStack (LoRaWAN Network Server) set up and running. You will need to configure InfluxDB and obtain the necessary InfluxDB token and URL.

## Steps to Run the Python Code

1. **Clone the Repository**:

   - Clone the repository containing the Python code to your local machine.

   ```bash
   git clone https://github.com/moheed-ali/ChirpStack-InfluxDB.git
   ```
2. **Create a Python Virtual Environment** (Recommended):

   - To isolate your project's dependencies, consider creating a Python virtual environment. This is especially useful when working on multiple Python projects with different dependencies.

   - Create a virtual environment using the following command:

     ```bash
     python -m venv myenv  # Replace 'myenv' with your preferred virtual environment name
     ```

   - Activate the virtual environment:

     ```bash
     source myenv/bin/activate  # Linux/Mac
     ```

     ```bash
     myenv\Scripts\activate  # Windows
     ```

   - Now, you can install and run the script (`main.py`) within the virtual environment. 

3. **Install Required Packages**:
   
   - Navigate to the project directory and install the required Python packages using pip.
    ```bash
   cd ChirpStack-InfluxDB
   pip install -r requirements.txt
   ```
4. **Edit Configuration:**:
   - `bucket`: The InfluxDB bucket where data will be stored. You should set this variable to the name of the InfluxDB bucket where you want to store the incoming data.

   - `org`: The InfluxDB organization. Set this variable to your InfluxDB organization's name.

   - `token`: The InfluxDB token for authentication. Replace this variable with your InfluxDB authentication token. You can obtain this token from your InfluxDB instance.

   - `url`: The URL of your InfluxDB instance. Update this variable to the URL of your InfluxDB server. The default value is often `http://localhost:8086` if running locally.

   - `csv_filename`: The name of the CSV file where data will be logged. You can specify a custom name for the CSV file where the script will log data.

5. **Save the Changes**:

   - After making the necessary modifications, save the Python script.
     
6. **Run The Script**:

   - After making the necessary modifications, save the Python script.
  
     ```bash
     python main.py    
     ```

**Note**: If you are using Python version less than 3.7, you may encounter an error indicating that the `builder.py` file is missing in one of the Google Protocol Buffers libraries. In such cases, you can follow these steps:

1. **Copy the `builder.py` File**:
   
   - Locate the `builder.py` file within the repository.

   - Copy the `builder.py` file to your clipboard.

3. **Paste the `builder.py` File**:

   - Navigate to the location where the missing `builder.py` file is required in your Python environment.

   - Paste the copied `builder.py` file into this location.

This should resolve the missing `builder.py` error when using Python versions less than 3.7.


For instructions on adding InfluxDB as a datasource in Grafana, please refer to the [Steps to Add InfluxDB as a Datasource in Grafana](influxdb-grafana-data-source-setup.md) section.


### Introduction

....


### Prerequisites

....

### Sample Queries

Here are some sample InfluxDB queries that you can use as a reference:

### HTTP Port
```bash
http://localhost:8081
```
or run the command:
```bash
ip addr
```
to find the IP address like : 
```bash
http://163.173.230.90:8081
```


### InfluxDB Port
```bash
http://localhost:8086
```
or run the command:
```bash
ip addr
```
to find the IP address like :
```bash
http://163.173.230.90:8086
```

### InfluxDB & Grafana Docker Volume Commands 
InfluxDB: 
```bash
docker run \
    --name influxdb \
    -p 8086:8086 \
    --volume location_in_the_host_file_system:/var/lib/influxdb2 \
    influxdb:2.0.9
```
For Example: 
```bash
docker run \
    --name influxdb \
    -p 8086:8086 \
    --volume \etudiants\siscol\k\kayan_mo\Documents\data\influxdb-docker-data-volume:/var/lib/influxdb2 \
    influxdb:2.0.9
```
Grafana: 
```bash
docker run \
    --name grafana \
    -p 3000:3000 \
    -v location_in_the_host_file_system:/var/lib/grafana \
    grafana/grafana:8.3.1
```
For Example: 
```bash
docker run \
    --name grafana \
    -p 3000:3000 \
    -v \etudiants\siscol\k\kayan_mo\Documents\data\grafana-docker-data-volume:/var/lib/grafana \
    grafana/grafana:8.3.1
```



## Flux Queries
#### Query 1: Devices PDR
```Flux

  from(bucket: "upevent")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "my_measurement")
  |> group(columns: ["Gateway_ID", "Spreading_factor"], mode: "by")
  |> unique(column: "Device_Name") 
  |> count(column: "Device_Name")
  |> map(fn: (r) => ({
    _time: r._time,
    Gateway_ID: r.Gateway_ID,
    Spreading_factor: r.Spreading_factor,
    No_of_Devices: r.Device_Name,
    //current_time: now(), // Add a column with the current time
  }))
  |> drop(columns: ["_value"])
  |> yield(name: "mean")
  
  
//  
  
total_missed = from(bucket: "upevent")
 |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
 |> filter(fn: (r) => r["_field"] == "F_count")
 |> group (columns: ["Device_Name"])
 |> sort(columns: ["_value"], desc: false)
 |> difference(nonNegative: false, columns: ["_value"])
 |> map(fn: (r) => ({r with _frame_missed: r._value - 1}))
 |> sum(column: "_frame_missed") 
 //|> yield(name: "result")

total_received = from(bucket: "upevent")
 |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
 |> filter(fn: (r) => r["_field"] == "F_count")
 |> group (columns: ["Device_Name"])
 |> count(column: "_value")
 |> rename(columns: {_value: "_total_received"})
 //|> yield(name: "result")


join(
  tables: {total_missed: total_missed, total_received: total_received},
  on: ["Device_Name"]
) 
|> map(fn: (r) => ({
   _time: now(),
   Device: r.Device_Name,
   PDR: if r._total_received == 0.0 then 0.0 else float(v:r._total_received) / (float(v: r._frame_missed) + float(v: r._total_received)) * 100.0
 }))
|> yield(name: "result")

``` 
#### Query 2: Total Number of Active Devices  

```Flux
from(bucket: "upevent")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "my_measurement")
  |> group(columns: ["Gateway_ID"])
  |> unique(column: "Device_Name") 
  |> count(column: "Device_Name")
  |> map(fn: (r) => ({
    _time: r._time,
    Gateway_ID: r.Gateway_ID,
    No_of_Devices: r.Device_Name,
  }))
  |> drop(columns: ["_value"])
  |> yield(name: "mean")

```
#### Query 3: No. of Devices In each SF of each Gateway 
```Flux
from(bucket: "upevent")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "my_measurement")
  |> group(columns: ["Gateway_ID", "Spreading_factor"], mode: "by")
  |> unique(column: "Device_Name") 
  |> count(column: "Device_Name")
  |> map(fn: (r) => ({
    _time: r._time,
    Gateway_ID: r.Gateway_ID,
    Spreading_factor: r.Spreading_factor,
    No_of_Devices: r.Device_Name,
  }))
  |> drop(columns: ["_value"])
  |> yield(name: "mean")
  
```
#### Task 1: Save PDR to new Bucket 
```Flux
option task = {
    name: "save_pdr",
    every: 5m,
}

total_missed = from(bucket: "upevent")
    |> range(start: -task.every)
    |> filter(fn: (r) => r["_field"] == "F_count")
    |> group(columns: ["Device_Name"])
    |> sort(columns: ["_value"], desc: false)
    |> difference(nonNegative: false, columns: ["_value"])
    |> map(fn: (r) => ({r with _frame_missed: r._value - 1}))
    |> sum(column: "_frame_missed")

//|> yield(name: "result")
total_received = from(bucket: "upevent")
    |> range(start: -task.every)
    |> filter(fn: (r) => r["_field"] == "F_count")
    |> group(columns: ["Device_Name"])
    |> count(column: "_value")
    |> rename(columns: {_value: "_total_received"})

//|> yield(name: "result")
join(
    tables: {total_missed: total_missed, total_received: total_received},
    on: ["Device_Name"],
)
    |> map(
        fn: (r) => ({
            _time: now(),
            _measurement: "PDR",
            _field: "Ratio",
            _Device: r.Device_Name,
            _value: if r._total_received == 0.0 then 0.0 else float(v: r._total_received) / (float(v: r._frame_missed) + float(v: r._total_received)) * 100.0,
        }),
    )
    |> to(bucket: "PDR", org: "elora") 
```
#### Query 4: PDR Over Time      
```Flux
from(bucket: "PDR")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "PDR")
  |> filter(fn: (r) => r["_field"] == "Ratio")
  |> group(columns: ["_Device"])
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean") 
```
#### Query 5: Network PDR      
```Flux
total_missed = from(bucket: "upevent")
 |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
 |> filter(fn: (r) => r["_field"] == "F_count")
 |> group (columns: ["Device_Name"])
 |> sort(columns: ["_value"], desc: false)
 |> difference(nonNegative: false, columns: ["_value"])
 |> map(fn: (r) => ({r with _frame_missed: r._value - 1}))
 |> sum(column: "_frame_missed") 
 //|> yield(name: "result")

total_received = from(bucket: "upevent")
 |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
 |> filter(fn: (r) => r["_field"] == "F_count")
 |> group (columns: ["Device_Name"])
 |> count(column: "_value")
 |> rename(columns: {_value: "_total_received"})
 //|> yield(name: "result")


combined_table = join(
  tables: {total_missed: total_missed, total_received: total_received},
  on: ["Device_Name"]
) 
|> map(fn: (r) => ({
   _time: now(),
   Device: r.Device_Name,
   sum_total_rec: r._total_received,
   sum_total_send: r._total_received + r._frame_missed
 }))
 
|> reduce(
   fn: (r, accumulator) => ({
     sum_total_rec: r.sum_total_rec + accumulator.sum_total_rec,
     sum_total_send: r.sum_total_send + accumulator.sum_total_send,
   }),
   identity: {sum_total_rec: 0, sum_total_send: 0}
 )
 
|> map(fn: (r) => ({
   _time: now(),
   Device: r.Device,
   Total_Packets_Received: r.sum_total_rec,
   Total_Packets_Send: r.sum_total_send,
   Total_Packets_Missed: r.sum_total_send - r.sum_total_rec,
   Ratio: (float(v: r.sum_total_rec) / float(v: r.sum_total_send)) * 100.0
 }))
|> yield(name: "result")
```
