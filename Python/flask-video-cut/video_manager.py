import os

VIDEO_FOLDER = 'static'

class VideoManager:
    def __init__(self):
        self.video_list = self._get_video_list()
        self.selected_video = None

    def _get_video_list(self):
        video_list = []
        for root, dirs, files in os.walk(VIDEO_FOLDER):
            for file in files:
                if file.endswith('.mp4'):
                    rel_dir = os.path.relpath(root, VIDEO_FOLDER)
                    if rel_dir == '.':
                        video_list.append(file)
                    else:
                        video_list.append(os.path.join(rel_dir, file))
        return video_list

    def get_video_list(self):
        return self._get_video_list()

    def get_selected_video(self):
        return self.selected_video

    def select_video(self, video_name):
        self.selected_video = video_name

    def next_video(self):
        current_index = self.video_list.index(self.selected_video)
        next_index = (current_index + 1) % len(self.video_list)
        self.selected_video = self.video_list[next_index]

    def previous_video(self):
        current_index = self.video_list.index(self.selected_video)
        previous_index = (current_index - 1) % len(self.video_list)
        self.selected_video = self.video_list[previous_index]
