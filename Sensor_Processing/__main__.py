import requests
from flask import Flask, render_template, request
#from HumanScreamDetect.RecordSound import record_sound
from HumanScreamDetect.RecordSound2 import record_sound
from camera import capture_and_save_image
import os

app = Flask(__name__, template_folder='./templates')
app.secret_key = "12345678"

# Get the directory containing the script (__main__.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Global variables to manage recording and image capturing
is_recording = False
previous_acc = 0
previous_sound = 0

TARGET_IP = '172.20.10.6'
TARGET_PORT = 5050

def capture_image():
    result = capture_and_save_image()
    if result:
        print("Image captured and saved successfully.")
    else:
        print("Failed to capture and save the image.")

    # Send the captured image to the other server
    if result:
        image_filename = "Sensor_Processing/static/images/test-python.jpg"
        
        files = {'file': open(image_filename, 'rb')}
        response = requests.post(f'http://{TARGET_IP}:{TARGET_PORT}/Uploads', files=files)
        if response.status_code == 200:
            print("Image uploaded to the other server successfully.")
        else:
            print("Failed to upload the image to the other server.")

def record():
    global is_recording
    is_recording = True  # Lock recording to prevent multiple simultaneous recordings
    #record_sound(44100, 10)
    record_sound()
    is_recording = False  # Unlock recording after it has ended

    # Send the recorded sound to the other server
    sound_filename = "Sensor_Processing/HumanScreamDetect/SoundRecord/recorded.wav"
    files = {'file': open(sound_filename, 'rb')}
    response = requests.post(f'http://{TARGET_IP}:{TARGET_PORT}/Uploads', files=files)
    if response.status_code == 200:
        print("Sound uploaded to the other server successfully.")
    else:
        print("Failed to upload the sound to the other server.")

@app.route('/manual_capture_image', methods=['GET', 'POST'])
def manual_capture_image():
    capture_image()

    return render_template('index.html')

@app.route('/manual_record_sound', methods=['GET', 'POST'])
def manual_record_sound():
    global is_recording

    if request.method == 'POST':
        # Check if recording is not already in progress
        if not is_recording:
            record()

        return 'Recording started'

    return 'Method not allowed'

@app.route('/')
@app.route('/home')
def index():
    """
    Render the index.html template.
    """
    return render_template('index.html')

@app.route('/data')
def transfer_data():
    """
    Handle data transfer and control recording and image capture.

    This function checks the provided data, controls recording, and captures an image when needed.
    """
    global previous_acc, previous_sound, is_recording  # Ensure we're modifying the global variables

    # Get the query parameters from the request
    ppm = request.args.get('p')
    sound = float(request.args.get('s'))
    acc = float(request.args.get('a'))

    response = requests.post(f'http://{TARGET_IP}:{TARGET_PORT}/data', json={'p': ppm})

    if response.status_code == 200:
        print("Update server successfully.")
    else:
        print("Failed to update to the server.")

    # Check if 'acc' changed from 2 to 0 or 2 to 1
    if (previous_acc == 2 and acc == 0) or (previous_acc == 2 and acc == 1):
        capture_image()

    # Check if 'sound' changes from 0 to 1 and recording is not already in progress
    if (previous_sound == 0 and sound == 1) and not is_recording:
        record()

    # Update the previous_acc and previous_sound variables
    previous_acc = acc
    previous_sound = sound

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
