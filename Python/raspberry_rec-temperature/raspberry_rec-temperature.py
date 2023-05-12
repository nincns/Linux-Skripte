#!/usr/bin/env python3

import os
import time

EXPORT_FOLDER = "/path/to/export/folder/"

def get_cpu_temperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return res.replace("temp=","").replace("'C\n","")

def get_gpu_temperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return res.replace("temp=","").replace("'C\n","")

def get_host_uptime():
    uptime = os.popen('uptime -s').read().strip()
    uptime_start = time.mktime(time.strptime(uptime, "%Y-%m-%d %H:%M:%S"))
    uptime_now = time.time()
    uptime_seconds = int(uptime_now - uptime_start)
    uptime_days, uptime_seconds = divmod(uptime_seconds, 86400)
    uptime_hours, uptime_seconds = divmod(uptime_seconds, 3600)
    uptime_minutes = int(uptime_seconds / 60)
    return uptime_days, uptime_hours, uptime_minutes

def get_file_name():
    current_date = time.strftime("%Y-%m-%d")
    return os.path.join(EXPORT_FOLDER, f"{current_date}-gpu-cpu.txt")

while True:
    cpu_temp = get_cpu_temperature()
    gpu_temp = get_gpu_temperature()
    uptime_days, uptime_hours, uptime_minutes = get_host_uptime()

    file_name = get_file_name()
    with open(file_name, 'a') as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        uptime_string = f"{uptime_days} days {uptime_hours} hours {uptime_minutes} minutes"
        f.write(f"Timestamp (Uptime): {timestamp} - Running Uptime {uptime_string}\n")
        f.write(f"CPU Temperature: {cpu_temp} °C\n")
        f.write(f"GPU Temperature: {gpu_temp} °C\n")
        f.write("\n")

    time.sleep(1)
	