import pandas as pd

# Function to clean CPU.csv
def clean_cpu_csv():
    df_cpu = pd.read_csv('cpu.csv')
    df_cpu.dropna(subset=['cpu'], inplace=True)
    df_cpu.to_csv('Clean/cpu.csv', index=False)

# Function to clean disk.csv
def clean_disk_csv():
    df_disk = pd.read_csv('disk.csv')
    df_disk.dropna(subset=['free'], inplace=True)
    df_disk.to_csv('Clean/disk.csv', index=False)

# Function to clean diskio.csv
def clean_diskio_csv():
    df_diskio = pd.read_csv('diskio.csv')
    df_diskio = df_diskio[df_diskio['name'] == 'diskio']
    df_diskio.to_csv('Clean/diskio.csv', index=False)

# Clean each CSV file
clean_cpu_csv()
clean_disk_csv()
clean_diskio_csv()
