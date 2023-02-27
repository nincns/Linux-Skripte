#!/bin/bash

# Fest codierte Variable mit dem Pfad zum Ordner, der umbenannt werden soll
root_dir="/path/to/folder"

# Funktion, um die Videoauflösung zu extrahieren
get_video_resolution() {
    ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$1"
}

# Funktion, um alle Dateien im Ordner und Unterordnern zu durchlaufen und umzubenennen
rename_files() {
    while IFS= read -r -d '' file_path; do
        # Erstelle den neuen Dateinamen mit Videoauflösung, Erstellungsdatum und Uhrzeit
        video_resolution=$(get_video_resolution "$file_path")
        width=$(echo "$video_resolution" | cut -d ',' -f 1)
        height=$(echo "$video_resolution" | cut -d ',' -f 2)
        creation_time=$(date -r "$file_path" +"%Y-%m-%d_%H-%M")
        new_filename="${width}x${height}_${creation_time}"

        # Füge einen Unterstrich zwischen der Videoauflösung und dem Erstellungsdatum hinzu
        new_filename=$(echo "$new_filename" | sed -r "s/(\d+)x(\d+)_/\1x\2_/")

        # Entferne Leerzeichen aus dem neuen Dateinamen
        new_filename=$(echo "$new_filename" | tr -d ' ')

        # Überprüfe, ob ein anderer Dateiname bereits den neuen Namen hat, und füge ggf. eine Nummer hinzu
        new_file_path="$root_dir/$new_filename.${file_path##*.}"
        counter=1
        while [ -e "$new_file_path" ]; do
            # Wenn der neue Dateiname dem ursprünglichen Dateinamen entspricht, überspringe die Datei
            if [ "$new_file_path" = "$file_path" ]; then
                echo "Umbenennen von: $file_path"
                echo "In: $new_file_path (Ursprünglicher Name, keine Änderung)"
                break
            fi

            # Wenn der neue Dateiname identisch mit einem bereits vorhandenen Dateinamen ist, füge eine Nummer hinzu
            if [ "$(basename "$new_file_path")" = "$(basename "$file_path")" ]; then
                new_filename="${new_filename}_${counter}"
                new_file_path="$root_dir/$new_filename.${file_path##*.}"
                counter=$((counter+1))
            else
                # Wenn der neue Dateiname nicht identisch mit einem bereits vorhandenen Dateinamen ist, benenne die Datei um
                echo "Umbenennen von: $file_path"
                echo "In: $new_file_path"
                mv "$file_path" "$new_file_path"
                break
            fi
        done
    done < <(find "$root_dir" -type f -print0)
}

# Aufruf der Funktion mit dem fest codierten Pfad
rename_files "$root_dir"
