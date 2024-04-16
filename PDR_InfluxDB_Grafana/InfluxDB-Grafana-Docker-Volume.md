## InfluxDB & Grafana Docker Volume

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

For instructions on adding InfluxDB as a datasource in Grafana, please refer to the [Steps to Add InfluxDB as a Datasource in Grafana](influxdb-grafana-data-source-setup.md) section.  

For instructions on computing PDR using Flux Queries, please refer to the [Flux Queries to Compute PDR](PDR-Flux-Queries.md) section.


