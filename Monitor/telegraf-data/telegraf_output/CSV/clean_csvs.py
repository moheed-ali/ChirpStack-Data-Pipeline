import pandas as pd

# Function to clean CPU.csv
def clean_cpu_csv():
    df_cpu = pd.read_csv('cpu.csv')
    df_cpu.dropna(subset=['cpu'], inplace=True)
    df_cpu.to_csv('Clean/cpu.csv', index=False)

# Function to clean disk.csv
def clean_disk_csv():
    df_disk = pd.read_csv('disk.csv')
    df_disk = df_disk[df_disk['name'] == 'disk']
    df_disk.to_csv('Clean/disk.csv', index=False)

# Function to clean diskio.csv
def clean_diskio_csv():
    df_diskio = pd.read_csv('diskio.csv')
    df_diskio = df_diskio[df_diskio['name'] == 'diskio']
    df_diskio.to_csv('Clean/diskio.csv', index=False)

# Function to clean mem.csv
def clean_mem_csv():
    df_mem = pd.read_csv('mem.csv')
    df_mem = df_mem[df_mem['name'] == 'mem']
    df_mem.to_csv('Clean/mem.csv', index=False)

def clean_net_csv():
    df_net = pd.read_csv('net.csv')
    df_net.dropna(subset=['bytes_recv', 'icmp_inaddrmaskreps'], how='all', inplace=True)
    df_net.to_csv('Clean/net.csv', index=False)

# Function to clean mem.csv
def clean_swap_csv():
    df_swap = pd.read_csv('swap.csv')
    df_swap = df_swap[df_swap['name'] == 'swap']
    df_swap.to_csv('Clean/swap.csv', index=False)
    
# Function to clean PRO.csv
def clean_pro_csv():
    df_pro = pd.read_csv('pro.csv')
    df_pro.dropna(subset=['total_threads'], inplace=True)
    df_pro.to_csv('Clean/pro.csv', index=False)    

# Clean each CSV file
clean_cpu_csv()
clean_disk_csv()
clean_diskio_csv()
clean_mem_csv()
clean_net_csv()
clean_pro_csv()
clean_swap_csv()