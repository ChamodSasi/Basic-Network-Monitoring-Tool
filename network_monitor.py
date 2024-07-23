import requests
import schedule
import time
from datetime import datetime

def load_hosts(filename='hosts.txt'):
    with open(filename) as file:
        return [line.strip() for line in file]

def check_host(host):
    try:
        response = requests.get(host, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def log_status(host, status):
    with open('network_status.log', 'a') as log_file:
        log_file.write(f'{datetime.now()} - {host} - {"UP" if status else "DOWN"}\n')

def monitor_hosts():
    hosts = load_hosts()
    for host in hosts:
        status = check_host(host)
        log_status(host, status)

# Schedule the monitor_hosts function to run every 5 minutes
schedule.every(5).minutes.do(monitor_hosts)

if __name__ == '__main__':
    print("Starting network monitoring tool...")
    monitor_hosts()  # Initial run
    while True:
        schedule.run_pending()
        time.sleep(1)
