def record_audio(duration):
    import sounddevice as sd
    import numpy as np
    from scipy.io.wavfile import write

    fs = 44100  # Sample rate
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished
    write('output.wav', fs, audio)  # Save as WAV file
    print("Recording finished.")

def play_audio(file_path):
    import sounddevice as sd
    from scipy.io.wavfile import read

    fs, data = read(file_path)
    sd.play(data, fs)
    sd.wait()  # Wait until audio is finished playing
    print("Playback finished.")