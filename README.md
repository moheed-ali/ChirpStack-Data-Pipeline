

## Prerequisites

Before you begin, ensure you have the following prerequisites:

- **Python Installed**: You need to have Python installed on your system. You can download Python from the [official website](https://www.python.org/downloads/).
- 
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
     python3 -m venv myenv  # Replace 'myenv' with your preferred virtual environment name
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
   cd ChirpStack-Data-Pipeline
   pip3 install -r requirements.txt
   ```
     
4. **Run The Script**:

   - After making the necessary modifications, save the Python script.
  
     ```bash
     python3 main.py    
     ```

**Note**: If you are using Python version less than 3.7, you may encounter an error indicating that the `builder.py` file is missing in one of the Google Protocol Buffers libraries. In such cases, you can follow these steps:

1. **Copy the `builder.py` File**:
   
   - Locate the `builder.py` file within the repository.

   - Copy the `builder.py` file to your clipboard.

3. **Paste the `builder.py` File**:

   - Navigate to the location where the missing `builder.py` file is required in your Python environment.

   - Paste the copied `builder.py` file into this location.

This should resolve the missing `builder.py` error when using Python versions less than 3.7.  

## Contributing

Feel free to contribute to this project by creating pull requests. For major changes, please open an issue first to discuss the proposed changes.

## License

This project is licensed under the [MIT License](LICENSE).

