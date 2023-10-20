import requests
import torch
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from AlphaPose.crowd_congestion_result import crowd_congestion_result
from HumanScreamDetect.ModelEval import process_file

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
ALLOWED_EXTENSIONS = {'wav', 'jpg'}

crown = '不擁擠'
scream = 0
TARGET_IP = ''
TARGET_PORT = 5000
c_id = 168
c_no = 1
DEFAULT_ROUTE_WAY = 'OT1'
is_leaving = True
leave_station_count = 0
enter_station_count = 0

# Check whether the file extension is legal
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image():
    global crown, leave_station_count, enter_station_count

    print("Processing Image.")

    # Call the crowd_congestion_result function to process crowd congestion results
    result = crowd_congestion_result(
        input_img=input_dir,
        work_dir=work_dir,
        output_dir=output_dir,
        hc_save_img=True,
        ar_save_img=True
    )

    try:
        print(f'擁擠程度: {result["test-python.jpg"]["final_level"]}')
        print(result)
        crown = result['test-python.jpg']["final_level"]
    except KeyError:
        print(f'Detect Fail: {result}')

    # The leaving and enter signal
    if is_leaving:
        leave_station_count += 1
    else:
        enter_station_count += 1

    # Send the POST request
    try:
        send_info = {
            'c_id': c_id,
            'route_way': DEFAULT_ROUTE_WAY,
            'leave_station': leave_station_count,
            'enter_station': enter_station_count
        }

        response = requests.post(f'http://{TARGET_IP}:{TARGET_PORT}/access_signals', json=send_info)
        if response.status_code == 200:
            print("Request sent successfully.")
        else:
            print(f"Request failed with status code {response.status_code}.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")



def process_sound():
    global scream

    print("Processing Sound.")

    valuation_result = process_file('Uploads/recorded.wav', model)

    # Convert NumPy boolean to Python boolean
    evaluation_result = bool(valuation_result)

    print(f'尖叫檢測: {evaluation_result}')
    scream = evaluation_result


# File upload route
@app.route('/Uploads', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file selected"

    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    if file and allowed_file(file.filename): 
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Determine the file type and call the appropriate asynchronous function
        if filename.endswith('.jpg'):
            if os.path.exists('static/images/test-python.jpg'):
                os.remove('static/images/test-python.jpg')

            os.rename('Uploads/test-python.jpg', 'static/images/test-python.jpg')
            process_image()
        elif filename.endswith('.wav'):
            if os.path.exists('static/images/test-python.jpg'):
                os.remove('static/images/test-python.jpg')

            process_sound()

        return "File uploaded successfully"
    else:
        return "This file type is not allowed to be uploaded"

@app.route('/data', methods=['POST', 'GET'])
def transfer_data():
    """
    Handle data transfer and control recording and image capture.

    This function checks the provided data, controls recording, and captures an image when needed.
    """
    global crown, scream

    # Get the query parameters from the request
    ppm = request.get_json()['p']

    send_info = {
        'c_id': c_id,
        'c_no': c_no,
        'air': ppm,
        'volume': scream,
        'pNum': crown
    }

    print(send_info)

    # Send the POST request
    try:
        response = requests.post(f'http://{TARGET_IP}:{TARGET_PORT}/carriage_info', json=send_info)
        if response.status_code == 200:
            print("Request sent successfully.")
        else:
            print(f"Request failed with status code {response.status_code}.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

@app.route('/update_variables', methods=['POST', 'GET'])
def update_variables():
    global c_id, c_no

    # Get the new values from the form
    new_c_id = int(request.form.get('c_id'))
    new_c_no = int(request.form.get('c_no'))

    # Update the backend variables
    c_id = new_c_id
    c_no = new_c_no

    print(f'Update Car ID: {c_id}')
    print(f'Update Car Number: {c_no}')

    # Redirect back to the form page
    return render_template(
        'index.html',
        c_id=c_id,
        c_no=c_no
    )

@app.route('/')
@app.route('/home')
def index():
    return render_template(
        'index.html',
        c_id = c_id,
        c_no = c_no
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)