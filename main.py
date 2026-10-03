import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import soundfile as sf
import librosa
import numpy as np
import os
import tempfile

SAMPLE_RATE = 16000
DURATION = 2

COMMANDS = ["ON", "OFF", "START", "STOP"]


THRESHOLD = 100.0


def extract_features(filename):

    audio, sr = librosa.load(
        filename,
        sr=SAMPLE_RATE,
        mono=True
    )

    
    audio, _ = librosa.effects.trim(audio)

    
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))

    
    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=13
    )

    
    return np.mean(mfcc, axis=1)


def load_templates():

    templates = {}

    for command in COMMANDS:

        filename = f"templates/{command.lower()}.wav"

        if os.path.exists(filename):
            templates[command] = extract_features(filename)

    return templates


def record_voice():

    status_label.config(
        text="Listening...",
        fg="orange"
    )

    root.update()

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    temp_file.close()

    sf.write(
        temp_file.name,
        audio,
        SAMPLE_RATE
    )

    return temp_file.name


def recognize_voice():

    templates = load_templates()

    if not templates:

        messagebox.showerror(
            "Error",
            "Voice templates were not found."
        )

        return

    try:

        filename = record_voice()

        test_features = extract_features(filename)

        distances = {}

        for command, template in templates.items():

            distance = np.linalg.norm(
                test_features - template
            )

            distances[command] = distance

        best_command = min(
            distances,
            key=distances.get
        )

        best_distance = distances[best_command]

        # Similarity indicator
        score = max(
            0,
            100 - (best_distance / THRESHOLD * 100)
        )

        if best_distance <= THRESHOLD:

            result_label.config(
                text=best_command,
                fg="green"
            )

            score_label.config(
                text=f"Similarity: {score:.1f}%"
            )

            status_label.config(
                text="Command recognized",
                fg="green"
            )

        else:

            result_label.config(
                text="UNKNOWN",
                fg="red"
            )

            score_label.config(
                text=f"Distance: {best_distance:.2f}"
            )

            status_label.config(
                text="Command not recognized",
                fg="red"
            )

        os.remove(filename)

    except Exception as error:

        messagebox.showerror(
            "Error",
            str(error)
        )




root = tk.Tk()

root.title("Voice Recognition System")
root.geometry("600x450")

root.configure(bg="#101820")


title = tk.Label(
    root,
    text="VOICE RECOGNITION SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#101820",
    fg="white"
)

title.pack(pady=30)


subtitle = tk.Label(
    root,
    text="MFCC + Template Matching",
    font=("Arial", 13),
    bg="#101820",
    fg="lightgray"
)

subtitle.pack()


status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 15),
    bg="#101820",
    fg="cyan"
)

status_label.pack(pady=30)


result_title = tk.Label(
    root,
    text="Recognized Command",
    font=("Arial", 14),
    bg="#101820",
    fg="white"
)

result_title.pack()


result_label = tk.Label(
    root,
    text="---",
    font=("Arial", 30, "bold"),
    bg="#101820",
    fg="white"
)

result_label.pack(pady=10)


score_label = tk.Label(
    root,
    text="Similarity: ---",
    font=("Arial", 13),
    bg="#101820",
    fg="lightgray"
)

score_label.pack(pady=10)


record_button = tk.Button(
    root,
    text="START RECOGNITION",
    font=("Arial", 14, "bold"),
    padx=25,
    pady=12,
    command=recognize_voice
)

record_button.pack(pady=30)


info = tk.Label(
    root,
    text="Commands: ON | OFF | START | STOP",
    font=("Arial", 11),
    bg="#101820",
    fg="gray"
)

info.pack()


root.mainloop()