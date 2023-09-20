
## Steps to Add InfluxDB as a Datasource in Grafana

1. **Login to Grafana**: Open your Grafana instance in a web browser and log in using your credentials.

2. **Access Datasources**: After logging in, you'll be on the Grafana home page. In the left sidebar, click on the "Configuration" gear icon, and then select "Data Sources" under the "Data Sources" section.

3. **Add a New Datasource**:

   - Click the "Add data source" button.

   - Choose "InfluxDB" from the list of available data sources.
  
   - Select "Flux" as the Query language 

4. **Configure the InfluxDB Datasource**:

   - **HTTP Settings**:
     - **Name**: Enter a name for your InfluxDB datasource.
     - **HTTP URL**: Enter the URL to your InfluxDB instance, typically `http://localhost:8086` if InfluxDB is running on the same machine as Grafana or provide the IP of the docker container.

   - **Authentication**:
     - If your InfluxDB instance requires authentication, check the "Basic Auth" box, and provide the username and password.

   - **InfluxDB Details**:
     - **Organization**: Enter the name of the InfluxDB Organization you want to connect to.
     - **Token**: Paste the Token from the InfluxDB
     - 
   - **Other Settings**:
     - You can configure additional settings like the HTTP method, access, and others as needed.

5. **Save & Test**:
   - Scroll down and click the "Save & Test" button to test the connection to your InfluxDB datasource. Grafana will attempt to connect to InfluxDB using the provided settings and display a success message if the connection is successful.

6. **Success**:
   - If the connection test is successful, you've successfully added InfluxDB as a datasource in Grafana.
      

For instructions on computing PDR using Flux Queries, please refer to the [Flux Queries to Compute PDR](PDR-Flux-Queries.md) section.
