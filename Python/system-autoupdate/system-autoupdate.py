import os
import subprocess
import time
from datetime import datetime

export_dir = "/path/to/log/directory"
update_time = "13:00"  # Format HH:MM, 24-Stunden-Format

while True:
    current_time = datetime.now().strftime("%H:%M")
    if current_time >= update_time:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(export_dir, f"update_log_{timestamp}.txt")
        with open(log_file, "w") as f:
            subprocess.run(["sudo", "apt-get", "update", "-y"], stdout=f, stderr=subprocess.STDOUT)
            subprocess.run(["sudo", "apt-get", "upgrade", "-y"], stdout=f, stderr=subprocess.STDOUT)
        # Nach der Aktualisierung die nächste Aktualisierung um 24 Stunden verschieben
        update_time = (datetime.strptime(update_time, "%H:%M") + timedelta(days=1)).strftime("%H:%M")
    time.sleep(300)
