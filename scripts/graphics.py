import numpy as np
import matplotlib.pyplot as plt
from scipy import signal # For square and sawtooth waves

# --- Parameters for visualization ---
frequency = 2  # Hz (low frequency for clear visualization of wave shape)
duration = 1   # seconds
sample_rate = 400 # High enough to make waves look smooth, simulating continuous generation
time = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# --- Generate waveforms ---
# Sine Wave: The purest and simplest periodic oscillation.
sine_wave = np.sin(2 * np.pi * frequency * time)

# Square Wave: Abruptly alternates between two values.
# duty=0.5 means 50% of the period is spent at the high value.
square_wave = signal.square(2 * np.pi * frequency * time, duty=0.5)

# Sawtooth Wave: Rises linearly and then drops sharply.
# width=1.0 for a standard rising sawtooth.
sawtooth_wave = signal.sawtooth(2 * np.pi * frequency * time, width=1.0)

# Triangle Wave: Rises and falls linearly, with smooth corners.
# width=0.5 for a symmetric triangle where the peak is in the middle of the cycle.
triangle_wave = signal.sawtooth(2 * np.pi * frequency * time, width=0.5)

# Noise (White Noise): Random amplitude values, no discernible pattern or pitch.
# `np.random.uniform` creates random numbers within a specified range (-1 to 1).
noise_wave = np.random.uniform(-1, 1, len(time))

# --- Plotting All Waveforms ---
plt.figure(figsize=(14, 12)) # Larger figure for multiple subplots

# Plot Sine Wave
plt.subplot(5, 1, 1) # 5 rows, 1 column, 1st plot
plt.plot(time, sine_wave, color='purple')
plt.title('Sine Wave')
plt.ylabel('Amplitude')
plt.grid(True)
plt.ylim(-1.2, 1.2) # Consistent Y-axis for comparison

# Plot Square Wave
plt.subplot(5, 1, 2) # 2nd plot
plt.plot(time, square_wave, color='green')
plt.title('Square Wave')
plt.ylabel('Amplitude')
plt.grid(True)
plt.ylim(-1.2, 1.2)

# Plot Sawtooth Wave
plt.subplot(5, 1, 3) # 3rd plot
plt.plot(time, sawtooth_wave, color='red')
plt.title('Sawtooth Wave')
plt.ylabel('Amplitude')
plt.grid(True)
plt.ylim(-1.2, 1.2)

# Plot Triangle Wave
plt.subplot(5, 1, 4) # 4th plot
plt.plot(time, triangle_wave, color='blue')
plt.title('Triangle Wave')
plt.ylabel('Amplitude')
plt.grid(True)
plt.ylim(-1.2, 1.2)

# Plot Noise Wave
plt.subplot(5, 1, 5) # 5th plot
plt.plot(time, noise_wave, color='gray')
plt.title('Noise Wave')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.ylim(-1.2, 1.2)

plt.tight_layout() # Adjust layout to prevent overlapping titles/labels
plt.show()
