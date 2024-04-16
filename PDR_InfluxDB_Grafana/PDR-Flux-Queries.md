
## Flux Queries

These Queries will Display the results on InfluxDB Or Grafana

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
