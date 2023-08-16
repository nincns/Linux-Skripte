import os
import sys
import subprocess

def is_mp4_valid(file_path):
    cmd = ["ffprobe", "-hide_banner", "-loglevel", "error", "-i", file_path]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def convert_to_mp4(file_path):
    if not os.path.exists(file_path):
        print(f"File '{file_path}' not found.")
        return

    _, ext = os.path.splitext(file_path)
    if ext.lower() == ".mp4":
        if is_mp4_valid(file_path):
            print("The MP4 file is already consistent.")
            return
        else:
            print("The MP4 file is inconsistent. Converting...")

    output_path = file_path.rsplit('.', 1)[0] + '.mp4'

    cmd = ["ffmpeg", "-i", file_path, "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental", output_path]
    try:
        subprocess.run(cmd, check=True)
        print("Conversion successful!")
    except subprocess.CalledProcessError:
        print("Error converting the file with ffmpeg.")
        return

    if file_path != output_path:
        try:
            os.remove(file_path)
            print(f"Original file '{file_path}' has been deleted.")
        except:
            print(f"Error deleting the file '{file_path}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the file you want to convert.")
    else:
        file_path = sys.argv[1]
        convert_to_mp4(file_path)
