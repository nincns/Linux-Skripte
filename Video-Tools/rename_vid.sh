#!/bin/bash

root_dir="/path/to/folder"

get_video_resolution() {
    ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$1"
}

rename_files() {
    while IFS= read -r -d '' file_path; do
        video_resolution=$(get_video_resolution "$file_path")
        width=$(echo "$video_resolution" | cut -d ',' -f 1)
        height=$(echo "$video_resolution" | cut -d ',' -f 2)
        creation_time=$(date -r "$file_path" +"%Y-%m-%d_%H-%M")
        new_filename="${width}x${height}_${creation_time}"

        new_filename=$(echo "$new_filename" | sed -r "s/(\d+)x(\d+)_/\1x\2_/")
        new_filename=$(echo "$new_filename" | tr -d ' ')

        new_file_path="$root_dir/$new_filename.${file_path##*.}"
        counter=1
        while [ -e "$new_file_path" ]; do
            if [ "$new_file_path" = "$file_path" ]; then
                echo "Umbenennen von: $file_path"
                echo "In: $new_file_path (Ursprünglicher Name, keine Änderung)"
                break
            fi

            if [ "$(basename "$new_file_path")" = "$(basename "$file_path")" ]; then
                new_filename="${new_filename}_${counter}"
                new_file_path="$root_dir/$new_filename.${file_path##*.}"
                counter=$((counter+1))
            else
                echo "Umbenennen von: $file_path"
                echo "In: $new_file_path"
                mv "$file_path" "$new_file_path"
                break
            fi
        done
    done < <(find "$root_dir" -type f -print0)
}

rename_files "$root_dir"
