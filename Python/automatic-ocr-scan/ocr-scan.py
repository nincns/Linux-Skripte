import os
import time
from PIL import Image
import pytesseract
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from shutil import move
from datetime import datetime

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(folder_to_track):
            if filename.endswith(".png") or filename.endswith(".tif"):
                src = folder_to_track + "/" + filename
                new_destination = folder_destination + "/" + filename
                img = Image.open(src)
                text = pytesseract.image_to_string(img, lang='eng')
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                with open(f"./new-scan/ocr_output_{timestamp}.rtf", "w") as f:
                    f.write(text)
                move(src, new_destination)

folder_to_track = './import'
folder_destination = './archive'
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
