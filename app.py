from flask import Flask, Response, render_template, request, send_from_directory, jsonify
import os
import config
from camera import SecurityCamera

app = Flask(__name__)
cam = SecurityCamera()


@app.route('/')
def index():
    return render_template('index.html', latest_photo=cam.latest_photo)


@app.route('/video_feed')
def video_feed():
    return Response(cam.generate_mjpeg(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/start', methods=['POST'])
def start():
    mode = request.form.get('mode')
    if mode:
        cam.start_mode(mode)
    return ("", 204)


@app.route('/stop_save', methods=['POST'])
def stop_save():
    msg = cam.stop_save()
    return jsonify({"message": msg})


@app.route('/reset', methods=['POST'])
def reset():
    msg = cam.reset()
    return jsonify({"message": msg})


@app.route('/latest_photo')
def latest_photo_api():
    return jsonify({"path": cam.latest_photo})


@app.route('/view_file')
def view_file_param():
    path = request.args.get('path')
    if path and os.path.exists(path):
        ext = path.split('.')[-1].lower()
        if ext in ['jpg', 'jpeg', 'png']:
            mimetype = 'image/' + ext
        elif ext in ['mp4']:
            mimetype = 'video/mp4'
        else:
            mimetype = 'application/octet-stream'
        return send_from_directory(os.path.dirname(path), os.path.basename(path), mimetype=mimetype)
    return "File not found", 404


@app.route('/file_lists')
def file_lists():
    photos = sorted(os.listdir(config.PHOTO_DIR), reverse=True) if os.path.exists(config.PHOTO_DIR) else []
    videos = sorted([f for f in os.listdir(config.VIDEO_DIR) if f.endswith('.mp4')], reverse=True) if os.path.exists(config.VIDEO_DIR) else []
    recordings = sorted(os.listdir(config.RECORD_DIR), reverse=True) if os.path.exists(config.RECORD_DIR) else []

    html = '<div class="file-section"><h3>📸 Photos</h3>'
    if not photos:
        html += '<p class="status-box">No photos captured yet.</p>'
    for f in photos:
        html += f'''
        <div class="file-item">
            <a href="/view/photos/{f}" target="_blank">{f}</a>
            <button class="delete-btn" onclick="deleteFile('photos', '{f}')">Delete</button>
        </div>'''
    html += '</div>'

    html += '<div class="file-section"><h3>🎥 Videos</h3>'
    if not videos:
        html += '<p class="status-box">No videos recorded yet.</p>'
    for f in videos:
        html += f'''
        <div class="file-item">
            <a href="/view/videos/{f}" target="_blank">{f}</a>
            <button class="delete-btn" onclick="deleteFile('videos', '{f}')">Delete</button>
        </div>'''
    html += '</div>'

    html += '<div class="file-section"><h3>📊 Logs / CSV</h3>'
    if not recordings:
        html += '<p class="status-box">No logs found.</p>'
    for f in recordings:
        html += f'''
        <div class="file-item">
            <a href="/view/recordings/{f}" target="_blank">{f}</a>
            <button class="delete-btn" onclick="deleteFile('recordings', '{f}')">Delete</button>
        </div>'''
    html += '</div>'

    return html


@app.route('/view/<folder>/<filename>')
def view_file_folder(folder, filename):
    folders = {"photos": config.PHOTO_DIR, "videos": config.VIDEO_DIR, "recordings": config.RECORD_DIR}
    if folder in folders:
        dir_path = folders[folder]
        file_path = os.path.join(dir_path, filename)
        if os.path.exists(file_path):
            ext = filename.split('.')[-1].lower()
            if ext in ['jpg', 'jpeg', 'png']:
                mimetype = 'image/' + ext
            elif ext in ['mp4']:
                mimetype = 'video/mp4'
            else:
                mimetype = 'text/csv' if ext == 'csv' else 'application/octet-stream'
            return send_from_directory(dir_path, filename, mimetype=mimetype)
    return "File not found", 404


@app.route('/delete/<folder>/<filename>', methods=['POST'])
def delete_file(folder, filename):
    folders = {"photos": config.PHOTO_DIR, "videos": config.VIDEO_DIR, "recordings": config.RECORD_DIR}
    if folder in folders:
        file_path = os.path.join(folders[folder], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return ("", 204)
        return "File not found", 404
    return "Folder not found", 404


if __name__ == "__main__":
    print(f"Starting server on http://{config.HOST}:{config.PORT}")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
