import numpy as np
import sounddevice as sd
import soundfile as sf
import time
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def generate_notes():
    """Generates a dictionary of note names to frequencies from A0 to C8."""
    import math

    # All note names in an octave
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']

    notes = {}
    for midi_note in range(21, 109):  # A0 (21) to C8 (108)
        freq = 440.0 * 2 ** ((midi_note - 69) / 12)
        name = note_names[midi_note % 12] + str(midi_note // 12 - 1)
        notes[name] = round(freq, 2)

    notes['REST'] = 0.0
    return notes

NOTES = generate_notes()

# (Note, Duration in seconds)
TETRIS_MELODY = [
    ('E4', 0.4), ('B3', 0.2), ('C4', 0.2), ('D4', 0.4),
    ('C4', 0.2), ('B3', 0.2), ('A3', 0.4), ('A3', 0.2),
    ('C4', 0.2), ('E4', 0.4), ('D4', 0.2), ('C4', 0.2),
    ('B3', 0.4), ('B3', 0.2), ('C4', 0.2), ('D4', 0.4),
    ('E4', 0.4), ('C4', 0.4), ('A3', 0.4), ('A3', 0.4),
]

# Constants
SAMPLE_RATE = 44100
DURATION = 1.0

# Waveform time array generator
def get_time_array(duration):
    return np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)

# Waveform generators
def square_wave(freq, amp, duty, t):
    return amp * np.where(np.mod(t * freq, 1) < duty, 1.0, -1.0)

def wave_channel(freq, amp, _, t):
    return amp * np.sin(2 * np.pi * freq * t)

def noise_channel(amp, _1, _2, t):
    return amp * np.random.uniform(-1, 1, t.shape)

def plot_waveform(waveform, title="waveform", duration_ms=10):
    """Plot a portion of the waveform for visualization."""
    num_samples = int(SAMPLE_RATE * (duration_ms / 1000))
    plt.figure(figsize=(10, 4))
    plt.plot(waveform[:num_samples])
    plt.title(title)
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def play_melody(melody, wave_funcs, amps=None, dutys=None, plot=False, zoom_ms=10, save=False, save_file="Melody_Waveform.wav"):
    full_waveform = []
    
    for note, dur in melody:
        freq = NOTES[note]
        samples = int(SAMPLE_RATE * dur)
        if freq == 0.0:
            samples = int(dur * 1000)
            full_waveform.append(np.zeros(samples))
            continue

        t = get_time_array(dur)
        wave = np.zeros(samples)
        for i, func in enumerate(wave_funcs):
            amp = amps[i] if amps else 0.5
            duty = dutys[i] if dutys else 0.5
            wave += func(freq, amp, duty, t)

        wave /= len(wave_funcs)
        full_waveform.append(wave)
        
    final_waveform = np.concatenate(full_waveform)
    if plot:
        plot_waveform(final_waveform, title="Full Melody Waveform", duration_ms=zoom_ms)
    if save:
        sf.write(save_file, final_waveform, SAMPLE_RATE)

    sd.play(final_waveform, samplerate=SAMPLE_RATE)
    sd.wait()

class MusicPlayerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GB Melody Player (Tetris)")
        self.channel_configs = [
            {"name": "Square 1", "active": tk.BooleanVar(value=True), "type": "square"},
            {"name": "Square 2", "active": tk.BooleanVar(value=True), "type": "square"},
            {"name": "Wave", "active": tk.BooleanVar(value=True), "type": "wave"},
            {"name": "Noise", "active": tk.BooleanVar(value=False), "type": "noise"}
        ]
        self.controls = []
        self.create_ui()

    def create_ui(self):
        ctrl_frame = ttk.Frame(self)
        ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        for idx, cfg in enumerate(self.channel_configs):
            frame = ttk.LabelFrame(ctrl_frame, text=cfg["name"])
            frame.pack(pady=5, fill=tk.X)

            ttk.Checkbutton(frame, text="Enable", variable=cfg["active"]).pack(anchor=tk.W)

            amp = tk.DoubleVar(value=0.5)
            duty = tk.DoubleVar(value=0.5)

            ttk.Label(frame, text="Amplitude").pack()
            ttk.Scale(frame, from_=0, to=1, variable=amp, orient="horizontal").pack()

            if cfg["type"] == "square":
                ttk.Label(frame, text="Duty").pack()
                ttk.Scale(frame, from_=0.1, to=0.9, variable=duty, orient="horizontal").pack()
            else:
                duty = None

            self.controls.append({"amp": amp, "duty": duty})

        # Buttons
        ttk.Button(ctrl_frame, text="Play Tetris Melody", command=self.play_melody).pack(pady=10)

    def play_melody(self):
        funcs = []
        amps = []
        dutys = []
        for cfg, ctrl in zip(self.channel_configs, self.controls):
            if not cfg["active"].get():
                continue
            dutys.append(ctrl["duty"].get() if ctrl["duty"] else 0.5)
            amps.append(ctrl["amp"].get())
            if (cfg["type"] == "square"):
                funcs.append(square_wave)
            elif (cfg["type"] == "wave"):
                funcs.append(wave_channel)
            elif (cfg["type"] == "noise"):
                funcs.append(noise_channel)

        if not funcs:
            printf("Select at least one channel!")
            return
        
        play_melody(TETRIS_MELODY, funcs, amps, dutys)

if __name__ == "__main__":
    app = MusicPlayerApp()
    app.mainloop()
