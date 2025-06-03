"""
    Generate common waveforms, play and show them
"""

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# Sampling configuration
duration = 1.0  # seconds
sampling_rate = 44100  # Hz
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Waveform generation functions
def sine_wave(freq=440, amp=0.5):
    return amp * np.sin(2 * np.pi * freq * t)

def square_wave(freq=440, amp=0.5, duty=0.5):
    return amp * np.where(np.mod(t * freq, 1) < duty, 1.0, -1.0)

def triangle_wave(freq=440, amp=0.5):
    return amp * (2 * np.abs(2 * (t * freq % 1) - 1) - 1)

def sawtooth_wave(freq=440, amp=0.5):
    return amp * (2 * (t * freq % 1) - 1)

def noise_wave(amp=0.5):
    return amp * np.random.uniform(-1, 1, t.shape)

# Generate and play each waveform
waveforms = {
    "Sine": sine_wave(),
    "Square": square_wave(),
    "Triangle": triangle_wave(),
    "Sawtooth": sawtooth_wave(),
    "Noise": noise_wave()
}

# Plot and play
fig, axs = plt.subplots(5, 1, figsize=(10, 8))
for i, (name, wave) in enumerate(waveforms.items()):
    axs[i].plot(t[:1000], wave[:1000])
    axs[i].set_title(f"{name} Wave")
    axs[i].set_ylim(-1.1, 1.1)
    axs[i].grid(True)
    print(f"Playing {name} wave...")
    sd.play(wave, samplerate=sampling_rate)
    sd.wait()

plt.tight_layout()
plt.show()
