# task1.py 
#SARA
import psutil
import time
import datetime
import os

def format_time(life_time ):
    try:
        return datetime.datetime.fromtimestamp(life_time).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return "N/A"

def monitor_processes(refresh_interval=5):
    while True:
        try:

            os.system('cls' if os.name == 'nt' else 'clear')  

            print(f"{'PID':>6}  {'Name':<25} {'Start Time':<20} {'Executable Path'}")
            print("=" * 80)

            for proc in psutil.process_iter(['pid', 'name', 'create_time', 'exe']):
                try:
                    pid = proc.info['pid']
                    name = proc.info['name'] or 'N/A'
                    start_time = format_time(proc.info['create_time'])
                    exe_path = proc.info['exe'] or 'N/A'

                    print(f"{pid:>6}  {name:<25} {start_time:<20} {exe_path}")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            time.sleep(refresh_interval)
            

        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
            break

if __name__ == "__main__":
    monitor_processes()