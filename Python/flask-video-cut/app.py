from flask import Flask, render_template, request, redirect, flash, jsonify
from werkzeug.utils import secure_filename
import os
import subprocess
from video_manager import VideoManager

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv', 'webm', 'flv', 'mov', 'mpg', 'mpeg', 'm4v', 'wmv', '3gp', 
                      '3g2', 'ogg', 'ogv', 'vob', 'ts', 'm2ts', 'rm', 'rmvb', 'divx', 'asf', 
                      'dat', 'mxf', 'mpegts'}
app.config["TEMPLATES_AUTO_RELOAD"] = True
video_manager = VideoManager()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    video_list = video_manager.get_video_list()
    selected_video = video_manager.get_selected_video()
    return render_template('index.html', video_list=video_list, selected_video=selected_video)

@app.route('/get_video_list', methods=['GET'])
def get_video_list():
    video_list = video_manager.get_video_list()
    return jsonify({'videos': video_list})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect('/')
    if file and allowed_file(file.filename):
        upload_path = request.form.get('upload_path', '')
        if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], upload_path)):
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], upload_path))
        filename = secure_filename(file.filename)
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_path, filename)
        file.save(full_path)
        subprocess.run(["python3", "convert_mp4.py", full_path])
        return redirect('/')
    else:
        flash('File type not allowed')
        return redirect('/')

@app.route('/delete-video', methods=['POST'])
def delete_video():
    video_name = request.form.get('video_name[]')
    if not video_name:
        return 'No video name provided', 400
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_name)
    if os.path.exists(video_path):
        os.remove(video_path)
        return 'Video deleted successfully', 200
    else:
        return 'Video not found', 404

@app.route('/play', methods=['POST'])
def play_video():
    video_name = request.form.get('video_name')
    video_manager.select_video(video_name)
    return 'Video selected: {}'.format(video_name)

@app.route('/control/start')
def start_video():
    return 'Video started'

@app.route('/control/pause')
def pause_video():
    return 'Video paused'

@app.route('/control/next')
def next_video():
    video_manager.next_video()
    return 'Next video selected'

@app.route('/control/previous')
def previous_video():
    video_manager.previous_video()
    return 'Previous video selected'

@app.route('/control/jump_forward')
def jump_forward():
    return 'Jumped forward'

@app.route('/control/jump_backward')
def jump_backward():
    return 'Jumped backward'

@app.route('/save_crop', methods=['POST'])
def save_crop():
    video_name = request.form['video_name']
    content = request.form['content']
    crop_file_name = f"{video_name}.crop"
    with open(crop_file_name, "w") as f:
        f.write(content)
    os.system(f"python3 movie-split.py {crop_file_name}")
    return "Saved and video split"

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.run(host='0.0.0.0', port=5000)
