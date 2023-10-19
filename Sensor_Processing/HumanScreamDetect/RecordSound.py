import numpy as np
import scipy.io.wavfile as wv
import sounddevice


def record_sound(sample_rate, seconds):
    print('Record Start')

    voice_record = sounddevice.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    print(voice_record)
    # Wait until the recording is finished
    sounddevice.wait()

    # Save as WAV file in 16-bit format
    wv.write('Sensor_Processing/HumanScreamDetect/SoundRecord/recorded.wav', sample_rate, voice_record)

    print('Record End')