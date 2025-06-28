import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- Parameters for the sine wave ---
amplitude_val = 1.0  # Max amplitude for the wave
frequency_val = 2.0  # Hz (cycles per second)
duration = 1.5       # seconds (show a few cycles)
sample_rate = 500    # Points per second for a smooth curve

# Generate time array
time = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate sine wave
# y(t) = A * sin(2 * pi * f * t)
waveform = amplitude_val * np.sin(2 * np.pi * frequency_val * time)

# --- Calculate Period for Annotation ---
period_val = 1 / frequency_val # T = 1/f

# --- Plotting ---
plt.figure(figsize=(12, 7))
plt.plot(time, waveform, color='blue', linewidth=2, label='Sine Wave')

# --- Add Grid and Axis Labels ---
plt.axhline(0, color='gray', linestyle='--', linewidth=0.7) # X-axis line
plt.axvline(0, color='gray', linestyle='--', linewidth=0.7) # Y-axis line
plt.grid(True, linestyle=':', alpha=0.6)
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Amplitude (Pressure Variation)', fontsize=12)
plt.title('Illustrating Waveform Fundamentals: Amplitude and Frequency', fontsize=14)
plt.ylim(-amplitude_val * 1.2, amplitude_val * 1.2) # Give some padding

# --- Annotate Amplitude ---
# Arrow from x-axis to peak
plt.annotate(
    '', xy=(0.25 / frequency_val, amplitude_val), xytext=(0.25 / frequency_val, 0),
    arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=8),
    ha='center', va='bottom'
)
# Arrow from x-axis to trough
plt.annotate(
    '', xy=(0.75 / frequency_val, -amplitude_val), xytext=(0.75 / frequency_val, 0),
    arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=8),
    ha='center', va='top'
)
plt.text(
    0.25 / frequency_val + 0.05, amplitude_val / 2, 'Amplitude',
    color='red', fontsize=12, ha='left', va='center', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2)
)
plt.text(
    0.75 / frequency_val + 0.05, -amplitude_val / 2, 'Amplitude',
    color='red', fontsize=12, ha='left', va='center', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2)
)
plt.text(
    duration * 0.85, amplitude_val * 0.8, 'Amplitude $\\leftrightarrow$ Volume',
    color='darkgreen', fontsize=13, ha='right', va='top', fontweight='bold',
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.5')
)


# --- Annotate Frequency/Period ---
# Draw horizontal arrow for one period
# Start at x=0, go to x=period_val, at a y slightly below the wave
y_period_arrow = -amplitude_val * 1.1
plt.annotate(
    '', xy=(period_val, y_period_arrow), xytext=(0, y_period_arrow),
    arrowprops=dict(facecolor='purple', shrink=0.05, width=1.5, headwidth=8),
    ha='center', va='bottom'
)
plt.text(
    period_val / 2, y_period_arrow - 0.1, f'Period (T = {period_val:.2f} s)',
    color='purple', fontsize=12, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2)
)

# Text for Frequency calculation
plt.text(
    period_val / 2, y_period_arrow - 0.35,
    f'Frequency (f) = 1 / T = 1 / {period_val:.2f} s = {frequency_val:.1f} Hz',
    color='purple', fontsize=12, ha='center', va='top',
    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2)
)

plt.text(
    duration * 0.85, amplitude_val * 0.6, 'Frequency $\\leftrightarrow$ Pitch',
    color='darkgreen', fontsize=13, ha='right', va='top', fontweight='bold',
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.5')
)


plt.tight_layout()
plt.show()

