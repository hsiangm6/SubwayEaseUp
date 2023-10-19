import torch
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from AlphaPose.crowd_congestion_result import crowd_congestion_result
from HumanScreamDetect.ModelEval import process_file
from HumanScreamDetect.RecordSound import record_sound

import os

app = Flask(__name__, template_folder='./templates')

app.secret_key = "12345678"
model = torch.load('HumanScreamDetect/Models/Resnet34_Model_2023-10-13--17-11-18.pt')

# Get the directory containing the script (__main__.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative paths
work_dir = os.path.join(script_dir, '..', 'AlphaPose')
input_dir = os.path.join(script_dir, 'static/images')
output_dir = os.path.join(script_dir, 'static')

# Convert the paths to the correct format (use forward slashes for consistency)
work_dir = work_dir.replace('\\', '/')
input_dir = input_dir.replace('\\', '/')
output_dir = output_dir.replace('\\', '/')

# Configuration file upload directory
UPLOAD_FOLDER = 'Uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# File types allowed to be uploaded
ALLOWED_EXTENSIONS = {'wav', 'jpeg'}


# Check whether the file extension is legal
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# File upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file selected"

    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "File uploaded successfully"
    else:
        return "This file type is not allowed to be uploaded"

@app.route('/')
@app.route('/home')
def index():
    return render_template(
        'index.html'
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)