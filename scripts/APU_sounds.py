import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sounddevice as sd

# Constants
SAMPLE_RATE = 44100
DURATION = 1.0
t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)

# Waveform generators
def square_wave(freq, amp, duty):
    return amp * np.where(np.mod(t * freq, 1) < duty, 1.0, -1.0)

def wave_channel(freq, amp):
    return amp * np.sin(2 * np.pi * freq * t)

def noise_channel(amp):
    return amp * np.random.uniform(-1, 1, t.shape)

class APUApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GameBoy APU Emulator")
        self.geometry("1000x600")

        # Channel configs
        self.channel_configs = [
            {"name": "Square 1", "active": tk.BooleanVar(value=True), "type": "square"},
            {"name": "Square 2", "active": tk.BooleanVar(value=True), "type": "square"},
            {"name": "Wave", "active": tk.BooleanVar(value=True), "type": "wave"},
            {"name": "Noise", "active": tk.BooleanVar(value=True), "type": "noise"}
        ]

        self.controls = []
        self.create_ui()
        self.update_plot()

    def create_ui(self):
        ctrl_frame = ttk.Frame(self)
        ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        for idx, cfg in enumerate(self.channel_configs):
            frame = ttk.LabelFrame(ctrl_frame, text=cfg["name"])
            frame.pack(pady=5, fill=tk.X)

            ttk.Checkbutton(frame, text="Enable", variable=cfg["active"], command=self.update_plot).pack(anchor=tk.W)

            freq = tk.DoubleVar(value=440 + idx * 110)
            amp = tk.DoubleVar(value=0.5)
            duty = tk.DoubleVar(value=0.5)

            ttk.Label(frame, text="Frequency").pack()
            ttk.Scale(frame, from_=100, to=1000, variable=freq, orient="horizontal", command=lambda e: self.update_plot()).pack()

            ttk.Label(frame, text="Amplitude").pack()
            ttk.Scale(frame, from_=0, to=1, variable=amp, orient="horizontal", command=lambda e: self.update_plot()).pack()

            if cfg["type"] == "square":
                ttk.Label(frame, text="Duty").pack()
                ttk.Scale(frame, from_=0.1, to=0.9, variable=duty, orient="horizontal", command=lambda e: self.update_plot()).pack()
            else:
                duty = None

            self.controls.append({"freq": freq, "amp": amp, "duty": duty})

        # Buttons
        ttk.Button(ctrl_frame, text="Play Sound", command=self.play_sound).pack(pady=10)

        # Plot
        fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def generate_wave(self, cfg, ctrl):
        if not cfg["active"].get():
            return np.zeros_like(t)

        freq = ctrl["freq"].get()
        amp = ctrl["amp"].get()
        duty = ctrl["duty"].get() if ctrl["duty"] else 0.5

        if cfg["type"] == "square":
            return square_wave(freq, amp, duty)
        elif cfg["type"] == "wave":
            return wave_channel(freq, amp)
        elif cfg["type"] == "noise":
            return noise_channel(amp)
        return np.zeros_like(t)

    def update_plot(self):
        self.ax.clear()
        mixed = np.zeros_like(t)

        for cfg, ctrl in zip(self.channel_configs, self.controls):
            mixed += self.generate_wave(cfg, ctrl)

        # Normalize
        mixed /= max(np.max(np.abs(mixed)), 1e-5)
        self.ax.plot(t[:1000], mixed[:1000])
        self.ax.set_title("APU Output (Zoomed)")
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.grid(True)
        self.canvas.draw()

    def play_sound(self):
        mixed = np.zeros_like(t)
        for cfg, ctrl in zip(self.channel_configs, self.controls):
            mixed += self.generate_wave(cfg, ctrl)
        mixed /= max(np.max(np.abs(mixed)), 1e-5)
        sd.play(mixed, samplerate=SAMPLE_RATE)
        sd.wait()

# Run app
if __name__ == "__main__":
    app = APUApp()
    app.mainloop()

