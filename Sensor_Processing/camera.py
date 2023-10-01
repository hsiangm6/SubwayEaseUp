import time
import libcamera
from picamera2 import Picamera2, Preview

def capture_and_save_image():
    try:
        directory = "Sensor_Processing/static/images"  # Specify the directory here
        picam = Picamera2()

        config = picam.create_preview_configuration(main={"size": (1600, 1200)})
        config["transform"] = libcamera.Transform(hflip=1, vflip=1)
        picam.configure(config)

        picam.start_preview(Preview.QTGL)

        picam.start()
        time.sleep(2)
        picam.capture_file(f"{directory}/test-python.jpg")

        picam.close()
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

# Usage
"""
result = capture_and_save_image()
if result:
    print("Image captured and saved successfully.")
else:
    print("Failed to capture and save the image.")
"""
