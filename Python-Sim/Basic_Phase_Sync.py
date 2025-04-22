import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

# Define the missing functions
def measure_phase_difference(signal1, signal2):
    # Get analytic signal (complex signal with real and imaginary parts)
    analytic_signal1 = hilbert(signal1)
    analytic_signal2 = hilbert(signal2)
    
    # Extract instantaneous phase
    phase1 = np.unwrap(np.angle(analytic_signal1))
    phase2 = np.unwrap(np.angle(analytic_signal2))
    
    # Calculate phase difference
    phase_diff = phase1 - phase2
    
    return phase_diff

def sync_phase_fft(signal_to_adjust, reference_signal):
    # Compute FFTs
    fft_ref = np.fft.fft(reference_signal)
    fft_adj = np.fft.fft(signal_to_adjust)
    
    # Get magnitudes and phases
    mag_adj = np.abs(fft_adj)
    phase_ref = np.angle(fft_ref)
    
    # Create new FFT using magnitude of signal_to_adjust but phase of reference
    fft_synced = mag_adj * np.exp(1j * phase_ref)
    
    # Convert back to time domain
    synced_signal = np.real(np.fft.ifft(fft_synced))
    
    return synced_signal

# Generate example signals - a mix of frequencies with phase offsets
fs = 1000  # Sample rate
t = np.arange(1000) / fs
# Reference signal - mix of 5Hz and 15Hz
reference = np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*15*t)
# Signal to synchronize - same frequencies but different phases
to_sync = np.sin(2*np.pi*5*t + 0.7) + 0.5*np.sin(2*np.pi*15*t + 1.2)

# Measure overall phase difference
phase_diff = measure_phase_difference(to_sync, reference)
avg_phase = np.mean(phase_diff)
print(f"Average phase difference: {avg_phase:.2f} radians")

# Synchronize using FFT method to preserve frequencies
synced_signal = sync_phase_fft(to_sync, reference)

# Plot results
plt.figure(figsize=(12, 10))
plt.subplot(311)
plt.plot(t, reference, label='Reference Signal')
plt.plot(t, to_sync, label='Signal with Phase Offset')
plt.legend()
plt.title('Original Signals')

plt.subplot(312)
plt.plot(t, phase_diff, label='Phase Difference')
plt.axhline(avg_phase, color='r', linestyle='--',
           label=f'Average Diff: {avg_phase:.2f} rad')
plt.legend()
plt.title('Phase Difference')

plt.subplot(313)
plt.plot(t, reference, label='Reference Signal')
plt.plot(t, synced_signal, label='Synchronized Signal')
plt.legend()
plt.title('After Phase Synchronization (Frequencies Preserved)')

plt.tight_layout()
plt.show()

# Verify frequency content is preserved
def plot_spectrum(signal, fs, label):
    spectrum = np.abs(np.fft.rfft(signal))
    freqs = np.fft.rfftfreq(len(signal), 1/fs)
    plt.plot(freqs, spectrum, label=label)

plt.figure(figsize=(10, 6))
plot_spectrum(to_sync, fs, "Original Signal")
plot_spectrum(synced_signal, fs, "Synchronized Signal")
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('Frequency Spectrum Comparison')
plt.legend()
plt.grid(True)
plt.show()