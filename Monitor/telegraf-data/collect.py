import subprocess
import schedule
import time

def copy_metrics():
    subprocess.run(['docker', 'cp', 'telegraf:/tmp/metrics.out', '/home/eleve/ChirpStack-Data-Pipeline/OUTPUT/metrics.out'])

# # Schedule the command to run every 100 milliseconds
schedule.every(10).seconds.do(copy_metrics)

# Schedule the command to run every hour
# schedule.every().hour.do(copy_metrics)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
