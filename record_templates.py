import sounddevice as sd
import soundfile as sf
import os
import time

SAMPLE_RATE = 16000
DURATION = 2

COMMANDS = ["ON", "OFF", "START", "STOP"]

os.makedirs("templates", exist_ok=True)

print("VOICE TEMPLATE RECORDING")
print("------------------------")

for command in COMMANDS:

    input(f"\nPress ENTER and say '{command}'...")

    print("Recording...")
    time.sleep(0.5)

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    filename = f"templates/{command.lower()}.wav"

    sf.write(filename, audio, SAMPLE_RATE)

    print(f"Saved: {filename}")

print("\nAll voice templates recorded successfully.")