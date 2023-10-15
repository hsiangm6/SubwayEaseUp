import torch
from flask import Flask, render_template, request

from HumanScreamDetect.ModelEval import process_file
from HumanScreamDetect.RecordSound import record_sound
from camera import capture_and_save_image

app = Flask(__name__, template_folder='./templates')

app.secret_key = "12345678"
model = torch.load('HumanScreamDetect/Models/Resnet34_Model_2023-10-13--17-11-18.pt')

# Initialize variables to track the previous state of 'acc' and 'sound'
previous_acc = 2
previous_sound = 0

@app.route('/')
@app.route('/home')
def index():
    return render_template(
        'index.html'
    )

@app.route('/data')
def transfer_data():
    global previous_acc, previous_sound  # Ensure we're modifying the global variables

    # Get the query parameters from the request
    ppm = request.args.get('p')
    sound = request.args.get('s')
    acc = request.args.get('a')

    # Check if 'acc' changed from 2 to 0 or 2 to 1
    if (previous_acc == 2 and acc == 0) or (previous_acc == 2 and acc == 1):
        result = capture_and_save_image()
        if result:
            print("Image captured and saved successfully.")



        else:
            print("Failed to capture and save the image.")

    # Check if 'sound' changes from 0 to 1
    if previous_sound == 0 and sound == 1:
        record_sound(44100, 10)
        evaluation_result = process_file('SoundRecord/recorded.wav', model)

        # Convert NumPy boolean to Python boolean
        evaluation_result = bool(evaluation_result)

        print(f'Sound Result: {evaluation_result}')

    # Update the previous_acc and previous_sound variables
    previous_acc = acc
    previous_sound = sound

    return render_template(
        'index.html'
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)