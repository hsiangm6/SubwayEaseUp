import os
def record_sound():
    print("Record end")
    os.system('arecord -D "plughw:2,0" -f dat -c 1 -r 44100 -d 10 Sensor_Processing/HumanScreamDetect/SoundRecord/recorded.wav')
    print("Record Start")