# #!/bin/bash
# # To Make the File Executable
# # chmod +x start.sh

# # Run Python files

# # Promethus Data Collection
# python3 /home/eleve/ChirpStack-Data-Pipeline/main.py &

# python3 /home/eleve/ChirpStack-Data-Pipeline/Promethus/prom_to.py &

# python3 /home/eleve/ChirpStack-Data-Pipeline/Monitor/telegraf-data/collect.py
# # echo "Python script executed successfully"
# # python3 file2.py &

# # Run C++ file
# # ./file3



#!/bin/bash
# Run Python files

# Function to stop processes
stop_processes() {
    echo -e "\e[31mStopping Python scripts...\e[0m"  # Red color for stopping message
    pkill -f "python3 /home/eleve/ChirpStack-Data-Pipeline/main.py"
    pkill -f "python3 /home/eleve/ChirpStack-Data-Pipeline/Promethus/prom_to.py"
    pkill -f "python3 /home/eleve/ChirpStack-Data-Pipeline/Monitor/telegraf-data/collect.py"
    echo -e "\e[32mPython scripts stopped.\e[0m"  # Green color for stopped message
}

# Trap SIGINT (Ctrl+C) and SIGTERM signals to stop processes before exiting
trap 'stop_processes; exit' SIGINT SIGTERM

# Start Python scripts
echo -e "\e[33mStarting Python scripts...\e[0m"  # Yellow color for starting message

python3 /home/eleve/ChirpStack-Data-Pipeline/main.py &
python3 /home/eleve/ChirpStack-Data-Pipeline/Promethus/prom_to.py &
python3 /home/eleve/ChirpStack-Data-Pipeline/Monitor/telegraf-data/collect.py &

# Wait for the processes to finish
wait
