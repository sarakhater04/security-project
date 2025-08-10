import logging
import csv
import time
import datetime
import psutil

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


class CSVFileHandler(logging.Handler):
    def __init__(self, filename):
        super().__init__()
        self.file = open(filename, mode="a", newline="")
        self.fieldnames = ['timestamp', 'pid', 'name', 'execution_time']
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        if self.file.tell() == 0:
            self.writer.writeheader()

    def emit(self, record):
        if isinstance(record.msg, dict):
            self.writer.writerow(record.msg)
            self.file.flush()


logger = logging.getLogger("csv_logger")
logger.setLevel(logging.INFO)
csv_handler = CSVFileHandler("system_logs.csv")
logger.addHandler(csv_handler)


for entry in get_process_data():
    logger.info(entry)
