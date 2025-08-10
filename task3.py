import psutil
import datetime
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

LOG_FILE = "activity_log.csv"
FIELDNAMES = ["timestamp", "pid", "name", "execution_time"]

# ========== PART 1: LOG PROCESS INFO ==========

def get_process_data():
    now = datetime.datetime.now()
    data = []
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            start_time = datetime.datetime.fromtimestamp(proc.info['create_time'])
            exec_time = str(now - start_time)
            data.append({
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "pid": pid,
                "name": name,
                "execution_time": exec_time
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return data

def write_to_csv(data):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"{len(data)} process records written to '{LOG_FILE}'.")

# ========== PART 2: ANALYSIS FUNCTIONS ==========

def analyze_repeated_processes():
    if not os.path.exists(LOG_FILE):
        print("[!] No log file found.")
        return

    df = pd.read_csv(LOG_FILE)
    df['rounded_time'] = pd.to_datetime(df['timestamp']).dt.strftime("%H:%M")

    grouped = df.groupby(['name', 'rounded_time']).size().reset_index(name='count')
    repeated = grouped[grouped['count'] > 3]

    print("\n🔁 [Repeated Processes At Same Time]")
    if repeated.empty:
        print("None found.")
    else:
        print(repeated)




def analyze_activity_spikes():
    if not os.path.exists(LOG_FILE):
        print("[!] No log file found.")
        return

    df = pd.read_csv(LOG_FILE)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['minute'] = df['timestamp'].dt.floor('T')

    spike_df = df.groupby('minute').size().reset_index(name='process_count')

    mean = spike_df['process_count'].mean()
    std = spike_df['process_count'].std()
    threshold = mean + 2 * std
    spikes = spike_df[spike_df['process_count'] > threshold]

    print("\n📈 [Unusual Activity Spikes]")
    if spikes.empty:
        print("No spikes detected.")
    else:
        print(spikes)

    plt.figure(figsize=(10, 5))
    plt.plot(spike_df['minute'], spike_df['process_count'], label='Process Count')
    plt.axhline(y=threshold, color='red', linestyle='--', label=f'Spike Threshold ({int(threshold)})')
    plt.title('Process Count Over Time')
    plt.xlabel('Time')
    plt.ylabel('Count')
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

# ========== MAIN MENU ==========

def main():
    while True:
        print("\n=== System Activity Monitor ===")
        print("1. Log current processes")
        print("2. Analyze repeated processes")
        print("3. Detect spikes in activity")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == '1':
            logs = get_process_data()
            write_to_csv(logs)
        elif choice == '2':
            analyze_repeated_processes()
        elif choice == '3':
            analyze_activity_spikes()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
