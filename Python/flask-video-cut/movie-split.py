import os
import moviepy.editor as mp

def convert_time_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    return hours * 3600 + minutes * 60 + seconds

def process_video(file, marks, output_path):
    video = mp.VideoFileClip(file)
    output_file = os.path.splitext(os.path.basename(file))[0]
    counter = 1
    for start, end in marks:
        subclip = video.subclip(start, end)
        subclip.write_videofile(os.path.join(output_path, output_file + "_" + str(counter) + ".mp4"), codec='libx264')
        counter += 1

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: movie-split.py <project-file>.crop")
        return

    project_file_path = sys.argv[1]
    
    with open(project_file_path, 'r') as f:
        lines = f.readlines()
    
    video_file_path = lines[-1].strip()
    marks = []
    for line in lines[:-1]:
        start_time_str, end_time_str = line.strip().split('-')
        start_time = convert_time_to_seconds(start_time_str)
        end_time = convert_time_to_seconds(end_time_str)
        marks.append((start_time, end_time))

    output_path_base = os.path.dirname(video_file_path)

    output_path = os.path.join(output_path_base, os.path.splitext(os.path.basename(project_file_path))[0])
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    process_video(video_file_path, marks, output_path)
    os.remove(project_file_path)

if __name__ == "__main__":
    main()
