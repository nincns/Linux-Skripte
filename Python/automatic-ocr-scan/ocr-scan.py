import os
import time
from PIL import Image
import pytesseract
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from shutil import move
from datetime import datetime

# Ordnerpfade als Variablen festlegen
folder_to_track = './import'
folder_destination = './archive'
folder_new_scan = './new-scan'

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(folder_to_track):
            if filename.endswith(".png") or filename.endswith(".tif"):
                src = os.path.join(folder_to_track, filename)
                new_destination = os.path.join(folder_destination, filename)
                img = Image.open(src)
                text = pytesseract.image_to_string(img, lang='eng')
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                with open(os.path.join(folder_new_scan, f"ocr_output_{timestamp}.rtf"), "w") as f:
                    f.write(text)
                move(src, new_destination)

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
