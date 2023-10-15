import torch
from flask import Flask, render_template, request

from AlphaPose.crowd_congestion_result import crowd_congestion_result
from HumanScreamDetect.ModelEval import process_file
from HumanScreamDetect.RecordSound import record_sound
from camera import capture_and_save_image

import os

app = Flask(__name__, template_folder='./templates')

app.secret_key = "12345678"
model = torch.load('HumanScreamDetect/Models/Resnet34_Model_2023-10-13--17-11-18.pt')

# Initialize variables to track the previous state of 'acc' and 'sound'
previous_acc = 2
previous_sound = 0

is_processing_photo = False
is_processing_sound = False

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

@app.route('/')
@app.route('/home')
def index():
    return render_template(
        'index.html'
    )


@app.route('/data')
def transfer_data():
    global previous_acc, previous_sound, is_processing_photo, is_processing_sound  # Ensure we're modifying the global variables

    # Get the query parameters from the request
    ppm = request.args.get('p')
    sound = request.args.get('s')
    acc = request.args.get('a')

    # Check if 'acc' changed from 2 to 0 or 2 to 1
    if ((previous_acc == 2 and acc == 0) or (previous_acc == 2 and acc == 1)) and not is_processing_photo:
        result = capture_and_save_image()
        if result and not is_processing_photo:
            is_processing_photo = True
            print("Image captured and saved successfully.")

            # Call the crowd_congestion_result function to process crowd congestion results
            result = crowd_congestion_result(
                input_img=input_dir,
                work_dir=work_dir,
                output_dir=output_dir,
                hc_save_img=True,
                ar_save_img=True
            )

            print(result['final_level'])
            is_processing_photo = False

        else:
            print("Failed to capture and save the image.")


    # Check if 'sound' changes from 0 to 1
    if (previous_sound == 0 and sound == 1) and not is_processing_sound:
        is_processing_sound = True
        record_sound(44100, 10)
        evaluation_result = process_file('HumanScreamDetect/SoundRecord/recorded.wav', model)

        # Convert NumPy boolean to Python boolean
        evaluation_result = bool(evaluation_result)

        print(f'Sound Result: {evaluation_result}')
        is_processing_sound = False

    # Update the previous_acc and previous_sound variables
    previous_acc = acc
    previous_sound = sound

    return render_template(
        'index.html'
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)