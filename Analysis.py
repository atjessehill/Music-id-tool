import librosa

def get_analysis(file):

    x, sr = librosa.load(file)

    tempo, beat_times = librosa.beat.beat_track(x, sr=sr)
