import os
import subprocess
import time
from datetime import datetime, timedelta

export_dir = "/path/to/log/autoupdate"
update_time = "12:40"  # Format HH:MM, 24-Stunden-Format

def calculate_wait_time(target_time_str):
    now = datetime.now()
    target_time = datetime.strptime(target_time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
    if target_time < now:  # target_time ist bereits vorbei, also planen wir für den nächsten Tag
        target_time += timedelta(days=1)
    wait_time_seconds = (target_time - now).total_seconds()
    if wait_time_seconds < 0:  # Falls die geplante Ausführungszeit in weniger als einer Stunde liegt
        wait_time_seconds += 24*60*60  # Füge 24 Stunden hinzu
    return wait_time_seconds

while True:
    wait_time = calculate_wait_time(update_time)
    print(f"Warten auf {wait_time} Sekunden bis zur nächsten Aktualisierung.")
    time.sleep(wait_time)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(export_dir, f"update_log_{timestamp}.txt")
    with open(log_file, "w") as f:
        subprocess.run(["sudo", "apt-get", "update", "-y"], stdout=f, stderr=subprocess.STDOUT)
        subprocess.run(["sudo", "apt-get", "upgrade", "-y"], stdout=f, stderr=subprocess.STDOUT)
