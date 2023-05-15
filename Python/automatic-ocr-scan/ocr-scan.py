import os
import time
import grp
import pwd
from PIL import Image
import pytesseract
from shutil import move
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

folder_to_track = '/home/smb-share/ocr-scan/import'
folder_destination = '/home/smb-share/ocr-scan/archive'
folder_new_scan = '/home/smb-share/ocr-scan/new-scan'
tesseract_lang = 'deu'

# Füge neuen Benutzer und Gruppe hinzu
user = 'nobody'
group = 'nogroup'
uid = pwd.getpwnam(user).pw_uid
gid = grp.getgrnam(group).gr_gid

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        convert_images()

def convert_images():
    for filename in os.listdir(folder_to_track):
        if filename.endswith((".png", ".tif", ".jpg", ".jpeg")):
            src = os.path.join(folder_to_track, filename)
            new_destination = os.path.join(folder_destination, filename)
            img = Image.open(src)
            text = pytesseract.image_to_string(img, lang=tesseract_lang)
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            new_file_path = os.path.join(folder_new_scan, f"ocr_output_{timestamp}.rtf")
            with open(new_file_path, "w") as f:
                f.write(text)
            move(src, new_destination)
            # Ändere Besitzer und Gruppe der neu erstellten Datei
            os.chown(new_file_path, uid, gid)
            # Ändere die Berechtigungen der neu erstellten Datei
            os.chmod(new_file_path, 0o755)

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
