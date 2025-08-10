import psutil

# Keywords to search for in process names, arguments, or memory
KNOWN_KEYLOGGER_INDICATORS = [
    "pynput", "keylogger", "keyboard", "listener", "hook", "inputlogger", "spy"
]

def detect_keyloggers():
    print(" Scanning processes for potential keyloggers...\n")
    suspicious_found = False

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            pid = proc.info['pid']
            name = (proc.info['name'] or '').lower()
            cmdline = ' '.join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ''

            # Detect suspicious name or cmdline
            if any(keyword in name for keyword in KNOWN_KEYLOGGER_INDICATORS) or \
               any(keyword in cmdline for keyword in KNOWN_KEYLOGGER_INDICATORS):
                print(f"⚠️ Suspicious process: PID={pid}, Name={name}, CMD={cmdline}")
                suspicious_found = True

            # Detect suspicious memory maps (like loaded pynput modules)
            try:
                for mmap in proc.memory_maps():
                    dll_path = mmap.path.lower()
                    if any(keyword in dll_path for keyword in KNOWN_KEYLOGGER_INDICATORS):
                        print(f"⚠️ Suspicious module in process: PID={pid}, DLL={dll_path}")
                        suspicious_found = True
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if not suspicious_found:
        print("✅ No suspicious keylogger processes found.")

if __name__ == "__main__":
    detect_keyloggers()
