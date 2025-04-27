# Phase Synchronization and Measurement

Some research into measuring phase differences between signals and achieving phase synchronization without altering frequency components.

## What is Phase Synchronization?

Phase synchronization happens when two oscillating signals maintain a constant phase relationship with each other. This guide focuses on methods that synchronize phase while preserving the original frequency content of signals.

## Measuring Phase Between Two Signals

### Basic Approach

1. **Extract the phase information** from each signal (Delay Time, Whether it's Leading/Lagging)
2. **Compare these phases** to determine their relationship

### Practical Methods

#### Using the Hilbert Transform

The most common approach for arbitrary signals:

```python
import numpy as np
from scipy.signal import hilbert

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
```

#### Using 🌊 Wavelet Decomposition

Analyze phase across multiple frequency scales and time points.

```python
import pywt

def wavelet_phase(signal, wavelet_name='cmor1.5-1.0', scales=np.arange(1, 128)):
    coefficients, _ = pywt.cwt(signal, scales, wavelet_name)
    phases = np.angle(coefficients)
    return phases
```
Phase difference:

```python
def wavelet_phase_difference(signal1, signal2, wavelet_name='cmor1.5-1.0', scales=np.arange(1, 128)):
    phase1 = wavelet_phase(signal1, wavelet_name, scales)
    phase2 = wavelet_phase(signal2, wavelet_name, scales)
    
    return phase1 - phase2
```
Visualize:
```python
import matplotlib.pyplot as plt

def plot_wavelet_phase_diff(phase_diff, scales):
    plt.figure(figsize=(10, 6))
    plt.imshow(phase_diff, aspect='auto', cmap='twilight', extent=[0, phase_diff.shape[1], scales[-1], scales[0]])
    plt.colorbar(label='Phase Difference (radians)')
    plt.title('Wavelet-Based Phase Difference')
    plt.xlabel('Time')
    plt.ylabel('Scale')
    plt.show()
```
#### For Specific Frequency Bands

If you need to analyze phase in specific frequency bands:

```python
from scipy import signal

def measure_phase_in_band(signal1, signal2, fs, freq_low, freq_high):
    # Design bandpass filter
    nyquist = 0.5 * fs
    low = freq_low / nyquist
    high = freq_high / nyquist
    b, a = signal.butter(4, [low, high], btype='band')
    
    # Apply filter
    filtered1 = signal.filtfilt(b, a, signal1)
    filtered2 = signal.filtfilt(b, a, signal2)
    
    # Get phase difference using filtered signals
    return measure_phase_difference(filtered1, filtered2)
```

## Synchronizing Two Signals (Frequency-Independent)

To synchronize signals based on their phase without changing frequency components:

### 1. Pure Phase Shifting Method

This applies a constant phase shift without affecting frequency:

```python
def phase_shift_signal(signal, phase_shift):
    """
    Shift the phase of a signal without changing its frequency components.
    
    Args:
        signal: Input signal
        phase_shift: Amount to shift the phase (in radians)
    
    Returns:
        Phase-shifted signal
    """
    # Get analytic signal
    analytic_signal = hilbert(signal)
    
    # Apply phase shift in the complex domain
    shifted_analytic = analytic_signal * np.exp(1j * phase_shift)
    
    # Take real part to get time-domain signal
    shifted_signal = np.real(shifted_analytic)
    
    return shifted_signal
```

### 2. Frequency-Domain Phase Synchronization

Using the Fast Fourier Transform (FFT) to preserve frequency content:

```python
def sync_phase_fft(signal_to_adjust, reference_signal):
    """
    Synchronize the phase of signal_to_adjust to match reference_signal,
    while preserving frequency content.
    """
    # Compute FFTs
    fft_ref = np.fft.fft(reference_signal)
    fft_adj = np.fft.fft(signal_to_adjust)
    
    # Get magnitudes and phases
    mag_ref = np.abs(fft_ref)
    mag_adj = np.abs(fft_adj)
    phase_ref = np.angle(fft_ref)
    
    # Create new FFT using magnitude of signal_to_adjust but phase of reference
    # This preserves frequency content but aligns phase
    fft_synced = mag_adj * np.exp(1j * phase_ref)
    
    # Convert back to time domain
    synced_signal = np.real(np.fft.ifft(fft_synced))
    
    return synced_signal
```

### 3. Constant Phase Offset Correction

For signals with approximately constant phase difference:

```python
def sync_with_constant_phase(signal_to_adjust, reference_signal):
    """
    Synchronize using a single, average phase offset.
    Preserves all frequency components.
    """
    # Measure phase difference
    phase_diff = measure_phase_difference(signal_to_adjust, reference_signal)
    
    # Calculate average phase difference
    avg_phase_diff = np.mean(phase_diff)
    
    # Apply constant phase shift
    synchronized_signal = phase_shift_signal(signal_to_adjust, -avg_phase_diff)
    
    return synchronized_signal
```

## Time Delay Method

Sometimes, phase differences come from simple time delays:

```python
def find_optimal_delay(signal1, signal2):
    """Find the time delay between two signals using cross-correlation"""
    correlation = np.correlate(signal1, signal2, mode='full')
    max_idx = np.argmax(correlation)
    delay = max_idx - (len(correlation) // 2)
    return delay

def sync_by_delay(signal_to_adjust, delay):
    """Shift signal in time to synchronize phases"""
    if delay > 0:
        # Shift right
        return np.concatenate([np.zeros(delay), signal_to_adjust[:-delay]])
    elif delay < 0:
        # Shift left
        return np.concatenate([signal_to_adjust[-delay:], np.zeros(-delay)])
    else:
        return signal_to_adjust
```

## Visualizing Phase Relationships

Plotting phase differences can help understand the relationship:

```python
import matplotlib.pyplot as plt

def plot_phase_relationship(signal1, signal2):
    # Extract phases
    phase1 = np.unwrap(np.angle(hilbert(signal1)))
    phase2 = np.unwrap(np.angle(hilbert(signal2)))
    phase_diff = phase1 - phase2
    
    # Plot time-domain signals
    plt.figure(figsize=(12, 8))
    plt.subplot(211)
    plt.plot(signal1, label='Signal 1')
    plt.plot(signal2, label='Signal 2')
    plt.legend()
    plt.title('Original Signals')
    
    # Plot phase difference
    plt.subplot(212)
    plt.plot(phase_diff)
    plt.title('Phase Difference Over Time')
    plt.xlabel('Sample')
    plt.ylabel('Phase Difference (radians)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Phase difference distribution
    plt.figure(figsize=(8, 6))
    plt.hist(phase_diff % (2*np.pi), bins=36)
    plt.title('Phase Difference Distribution')
    plt.xlabel('Phase Difference (radians)')
    plt.grid(True)
    plt.show()
```

## Complete Example: Frequency-Independent Phase Sync

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

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
```

## 🚀 Bonus: Wavelet Coherence 🔥

- Wavelet coherence detects how strongly two signals are phase-locked at each time and frequency.

#### Simple idea:

- Perform CWT on both signals
- Cross-multiply one by the conjugate of the other
- Normalize

## Common Challenges

- **Non-stationary signals**: Phase relationships may change over time
- **Noise interference**: Can cause inaccurate phase estimates
- **Multiple frequency components**: May need to synchronize different bands separately
- **Phase wrapping**: Be careful when averaging phase differences
- **Edge effects**: Hilbert transform has edge artifacts

## Practical Tips

1. **Filter first** if your signals are noisy
2. **Unwrap phases** when calculating differences
3. **Segment analysis** if phase relationships vary over time
4. **Validate results** by comparing time-domain signals before and after synchronization
5. **Check spectrograms** to ensure frequency components remain unchanged
