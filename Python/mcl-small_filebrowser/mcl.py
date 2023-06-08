#!/usr/bin/env python3
# MCL Midnight Commander Light by Steve Hentschke
import os
import curses
from datetime import datetime
import subprocess
import zipfile
import shutil

# Function for copying files or directories
def copy_item(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        if os.path.exists(dst):
            base_dir = os.path.dirname(dst)
            filename, extension = os.path.splitext(os.path.basename(dst))
            counter = 1
            while os.path.exists(dst):
                new_filename = f"{filename}_{counter}{extension}"
                dst = os.path.join(base_dir, new_filename)
                counter += 1
            shutil.copy2(src, dst)
        else:
            shutil.copy2(src, dst)

# Function for deleting files or directories
def delete_item(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

# Function for zipping an entire directory
def zipdir(path, ziph):
    """Zip an entire directory."""
    for root, dirs, files in os.walk(path):
        for file in files:
            # Ignore the current directory in the paths
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(
                    os.path.join(root, file),
                    os.path.join(path, '..')
                )
            )

# Function for creating a zip archive for the selected file or folder
def zip_file_or_folder(screen, current_dir, selected_item):
    """Create a zip archive for the selected file or folder."""
    path = os.path.join(current_dir, selected_item)
    zip_name = f"{selected_item}.zip"
    zip_path = os.path.join(current_dir, zip_name)

    if os.path.exists(zip_path):
        screen.addstr(0, 0, f"ZIP archive '{zip_name}' already exists.\n")
        screen.addstr(1, 0, "Do you want to replace it? (y/n)")
        screen.refresh()
        replace = screen.getch()
        if replace != ord('y'):
            return

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if os.path.isfile(path):
            # If the selected item is a file, add it to the zip archive
            zipf.write(path, os.path.basename(path))
        else:
            # If the selected item is a folder, zip the entire folder
            zipdir(path, zipf)

    screen.addstr(0, 0, f"ZIP archive '{zip_name}' created successfully.")
    screen.getch()

# Function for extracting the selected zip archive
def unzip_file(screen, current_dir, selected_item):
    """Unzip the selected zip archive."""
    path = os.path.join(current_dir, selected_item)

    if not zipfile.is_zipfile(path):
        screen.addstr(0, 0, f"'{selected_item}' is not a ZIP archive.")
        screen.getch()
        return

    with zipfile.ZipFile(path, 'r') as zipf:
        zipf.extractall(current_dir)

    screen.addstr(0, 0, f"ZIP archive '{selected_item}' extracted successfully.")
    screen.getch()

# Function for editing a file
def edit_file(screen, current_dir, selected_item):
    path = os.path.join(current_dir, selected_item)

    if os.path.isdir(path):
        screen.addstr(0, 0, f"'{selected_item}' is a directory.")
        screen.getch()
        return

    # Invoke nano as a subprocess to edit the file
    subprocess.call(['nano', path])

    # Redraw the screen after nano has exited
    screen.clear()
    screen.refresh()

# Function for displaying metadata
def display_metadata(screen, metadata):
    screen.clear()
    for key, value in metadata.items():
        screen.addstr(f"{key}: {value}\n")
    screen.getch()  # Wait for user input before returning to the directory screen

# Function for converting file size to KB, MB, GB, TB
def convert_size(size):
    """ Convert size in bytes to KB, MB, GB, TB """
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:8.1f} {unit}"
        size /= 1024.0

# Function for browsing a directory
def browse_directory(screen):
    selected_path_for_copy_move = None
    current_dir = os.getcwd()
    show_hidden = True
    selected_option = 0
    scroll_offset = 0
    max_items = screen.getmaxyx()[0] - 14  # Maximum lines minus some for displaying current directory and placeholders

    # Color configuration for curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        screen.clear()
        screen.addstr(0, 0, "Current Directory: " + current_dir)

        if selected_path_for_copy_move is not None:
            selected_path, copy_or_move = selected_path_for_copy_move
            screen.addstr(1, 0, f"{copy_or_move} selected: " + selected_path)

        dirs = []
        files = []

        for entry in os.scandir(current_dir):
            if show_hidden or not entry.name.startswith('.'):
                size = convert_size(entry.stat().st_size)
                created_time = os.path.getctime(entry)
                created_time = datetime.fromtimestamp(created_time).strftime("%d %b %Y %H:%M")
                item = (entry.name, size, created_time)
                if entry.is_dir():
                    dirs.append(item)
                elif entry.is_file():
                    files.append(item)

        dirs.sort()
        files.sort()

        items = [("...", "", "")] + dirs + files

        if selected_option - scroll_offset >= max_items:
            scroll_offset += 1
        elif selected_option - scroll_offset < 0 and scroll_offset > 0:
            scroll_offset -= 1

        for i, (name, size, created_time) in enumerate(items[scroll_offset:scroll_offset+max_items]):
            if i + scroll_offset == selected_option:
                screen.addstr(i+3, 0, "{:<20} {:<16} {}".format(created_time, size, name), curses.A_REVERSE)
            else:
                screen.addstr(i+3, 0, "{:<20} {:<16} {}".format(created_time, size, name))

        # Placeholder functions
        function_names = ["Zip", "Unzip", "View", "Edit", "Copy", "Move", "Paste", "Delete", "Quit"]
        for i, name in enumerate(function_names):
            screen.addstr(max_items+5, 0, " ".join([f"({i+1}) {name}" for i, name in enumerate(function_names)]))

        screen.refresh()

        key = screen.getch()

        if key == curses.KEY_UP and selected_option > 0:
            selected_option -= 1
        elif key == curses.KEY_DOWN and selected_option < len(items) - 1:
            selected_option += 1
        elif key == ord('\n'):
            if selected_option == 0:
                current_dir = os.path.dirname(current_dir)
            elif os.path.isdir(os.path.join(current_dir, items[selected_option][0])):
                current_dir = os.path.join(current_dir, items[selected_option][0])
        elif key == ord('1'):  # zip
            zip_file_or_folder(screen, current_dir, items[selected_option][0])
        elif key == ord('2'):  # unzip
            unzip_file(screen, current_dir, items[selected_option][0])
        elif key == ord('3'):  # View
            if not os.path.isdir(os.path.join(current_dir, items[selected_option][0])):
                screen.clear()
                try:
                    with open(os.path.join(current_dir, items[selected_option][0]), 'r') as f:
                        lines = f.readlines()
                except Exception as e:
                    screen.addstr(0, 0, f'Error: could not display file: {e}')
                    screen.getch()
                    continue

                scroll_offset_file = 0
                max_lines = screen.getmaxyx()[0] - 1  # Maximum lines minus 1 for displaying the prompt at the bottom
                while True:
                    screen.clear()
                    for i, line in enumerate(lines[scroll_offset_file:scroll_offset_file+max_lines]):
                        screen.addstr(i, 0, line.rstrip())
                    screen.addstr(max_lines, 0, 'Press q to quit, arrow keys to scroll.')
                    screen.refresh()

                    key = screen.getch()
                    if key == ord('q'):
                        break
                    elif key == curses.KEY_UP and scroll_offset_file > 0:
                        scroll_offset_file -= 1
                    elif key == curses.KEY_DOWN and scroll_offset_file < len(lines) - max_lines:
                        scroll_offset_file += 1

                # Reset selected option and scroll offset after viewing a file
                selected_option = 0
                scroll_offset = 0

        elif key == ord('4'):  # Edit
            edit_file(screen, current_dir, items[selected_option][0])

        elif key == ord('5'):  # Copy
            selected_path_for_copy_move = (os.path.join(current_dir, items[selected_option][0]), "copy")
        elif key == ord('6'):  # Move
            selected_path_for_copy_move = (os.path.join(current_dir, items[selected_option][0]), "move")
        elif key == ord('7'):  # Paste
            if selected_path_for_copy_move is not None:
                src_path, action = selected_path_for_copy_move
                dst_path = os.path.join(current_dir, os.path.basename(src_path))
                if action == "copy":
                    copy_item(src_path, dst_path)
                else:
                    copy_item(src_path, dst_path)
                    delete_item(src_path)
                selected_path_for_copy_move = None
            pass  # Your action here
        elif key == ord('8'):  # Delete
            item_to_delete = os.path.join(current_dir, items[selected_option][0])
            trash_dir = "/tmp/trash"
            # If /tmp/trash doesn't exist, create it
            if not os.path.exists(trash_dir):
                os.mkdir(trash_dir)

            # New path for the file/folder to be deleted
            new_path = os.path.join(trash_dir, items[selected_option][0])

            # Check if the path already exists, if yes, create a unique path
            if os.path.exists(new_path):
                base, ext = os.path.splitext(new_path)
                i = 1
                while os.path.exists(new_path):
                    new_path = base + "_" + str(i) + ext
                    i += 1

            shutil.move(item_to_delete, new_path)
            screen.addstr(1, 0, f"'{item_to_delete}' moved to /tmp/trash.")

        elif key == ord('9'):  # Quit
            break

curses.wrapper(browse_directory)
