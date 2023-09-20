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

For instructions on running InfluxDB & Grafana Docker Volumes, please refer to the [Steps to Add Run InfluxDB & Grafana Docker Volumes](InfluxDB-Grafana-Docker-Volume.md) section.  

For instructions on adding InfluxDB as a datasource in Grafana, please refer to the [Steps to Add InfluxDB as a Datasource in Grafana](influxdb-grafana-data-source-setup.md) section.  

For instructions on computing PDR using Flux Queries, please refer to the [Flux Queries to Compute PDR](PDR-Flux-Queries.md) section.


