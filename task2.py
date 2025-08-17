import psutil
import socket
import datetime
import time
#one two three
# List of common/safe ports (HTTP, HTTPS, DNS, etc.)
COMMON_PORTS = {80, 443, 53, 22, 25, 110, 143}

# Dummy suspicious IP list (you can expand this)
SUSPICIOUS_IPS = {
    "123.45.67.89", 
    "185.220.101.1"  # known TOR exit node 
}

def is_public_ip(ip):
    try:
        ip_parts = list(map(int, ip.split('.')))
        # Check for private IP ranges
        if (
            ip_parts[0] == 10 or
            (ip_parts[0] == 172 and 16 <= ip_parts[1] <= 31) or
            (ip_parts[0] == 192 and ip_parts[1] == 168)
        ):
            return False
        return True
    except:
        return False

def monitor_connections(refresh_interval=5):
    print("Starting network connection monitor...\n")
    while True:
        try:
            print(f"\n{'Time':<20} {'App':<25} {'Remote IP':<18} {'Port':<6} {'Alert'}")
            print("=" * 80)

            for conn in psutil.net_connections(kind='inet'):
                if conn.raddr:
                    ip = conn.raddr.ip
                    port = conn.raddr.port
                    pid = conn.pid

                    alert = ""

                    # Check if port is uncommon
                    if port not in COMMON_PORTS:
                        alert += "Uncommon Port "

                    # Check if IP is suspicious
                    if ip in SUSPICIOUS_IPS:
                        alert += "Suspicious IP "
                    elif is_public_ip(ip):
                        alert += ""  # Optional: flag all public IPs if needed

                    # Get process name
                    try:
                        proc = psutil.Process(pid)
                        app_name = proc.name()
                    except Exception:
                        app_name = "N/A"

                    # Format output
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"{timestamp:<20} {app_name:<25} {ip:<18} {port:<6} {alert.strip()}")

            time.sleep(refresh_interval)

        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
            break

if __name__ == "__main__":
    monitor_connections()
