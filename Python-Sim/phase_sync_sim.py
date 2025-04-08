import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pywt
from scipy.signal import hilbert
from scipy.interpolate import interp1d

class PhaseSync:
    def __init__(self, fs=1000):
        """
        Initialize the Phase Synchronizer with sampling frequency
        
        Parameters:
        -----------
        fs : float
            Sampling frequency in Hz
        """
        self.fs = fs
        self.buffer_size = int(fs * 5)  # 5 seconds buffer
        self.reference_buffer = np.zeros(self.buffer_size)
        self.target_buffer = np.zeros(self.buffer_size)
        self.sync_buffer = np.zeros(self.buffer_size)
        self.max_delay = int(0.5 * fs)  # Maximum delay of 500ms
        self.current_delay = 0
        self.wavelet = 'db4'  # Daubechies wavelet
        self.wavelet_level = 4
        
    def update_buffers(self, reference_signal, target_signal):
        """
        Update internal buffers with new signal data
        
        Parameters:
        -----------
        reference_signal : array-like
            Reference signal to synchronize to
        target_signal : array-like
            Target signal to be synchronized
        """
        if len(reference_signal) != len(target_signal):
            raise ValueError("Reference and target signals must have the same length")
            
        signal_length = len(reference_signal)
        
        # Shift old data to make room for new data
        self.reference_buffer = np.roll(self.reference_buffer, -signal_length)
        self.target_buffer = np.roll(self.target_buffer, -signal_length)
        
        # Add new data
        self.reference_buffer[-signal_length:] = reference_signal
        self.target_buffer[-signal_length:] = target_signal
    
    def detect_phase_difference_crosscorrelation(self):
        """
        Detect phase difference using cross-correlation
        
        Returns:
        --------
        phase_diff : float
            Phase difference in samples
        """
        # Use 1-second chunks for correlation
        chunk_size = self.fs
        ref_chunk = self.reference_buffer[-chunk_size:]
        target_chunk = self.target_buffer[-chunk_size:]
        
        # Normalize signals for better correlation
        ref_norm = (ref_chunk - np.mean(ref_chunk)) / (np.std(ref_chunk) + 1e-10)
        target_norm = (target_chunk - np.mean(target_chunk)) / (np.std(target_chunk) + 1e-10)
        
        # Compute cross-correlation
        correlation = signal.correlate(ref_norm, target_norm, mode='full')
        
        # Find the lag with maximum correlation
        max_idx = np.argmax(correlation)
        lag = max_idx - (len(ref_norm) - 1)
        
        return lag
    
    def detect_phase_difference_hilbert(self):
        """
        Detect phase difference using Hilbert transform
        
        Returns:
        --------
        phase_diff : float
            Phase difference in radians
        """
        # Get the latest 1-second of data
        window_size = self.fs
        ref_window = self.reference_buffer[-window_size:]
        target_window = self.target_buffer[-window_size:]
        
        # Apply Hilbert transform to get analytic signal
        ref_analytic = hilbert(ref_window)
        target_analytic = hilbert(target_window)
        
        # Extract instantaneous phase
        ref_phase = np.unwrap(np.angle(ref_analytic))
        target_phase = np.unwrap(np.angle(target_analytic))
        
        # Calculate phase difference
        phase_diff = np.mean(ref_phase - target_phase)
        
        # Convert to samples
        samples_diff = int((phase_diff / (2 * np.pi)) * window_size)
        
        return samples_diff
    
    def detect_phase_difference_wavelet(self):
        """
        Detect phase difference using wavelet decomposition for biosignals
        
        Returns:
        --------
        phase_diff : float
            Phase difference in samples
        """
        # Extract recent data for analysis
        window_size = self.fs * 2  # 2 seconds
        ref_window = self.reference_buffer[-window_size:]
        target_window = self.target_buffer[-window_size:]
        
        # Apply wavelet decomposition
        ref_coeffs = pywt.wavedec(ref_window, self.wavelet, level=self.wavelet_level)
        target_coeffs = pywt.wavedec(target_window, self.wavelet, level=self.wavelet_level)
        
        # Focus on approximation coefficients (lowest frequency band)
        ref_approx = ref_coeffs[0]
        target_approx = target_coeffs[0]
        
        # Normalize
        ref_approx = (ref_approx - np.mean(ref_approx)) / (np.std(ref_approx) + 1e-10)
        target_approx = (target_approx - np.mean(target_approx)) / (np.std(target_approx) + 1e-10)
        
        # Compute cross-correlation on wavelet coefficients
        correlation = signal.correlate(ref_approx, target_approx, mode='full')
        max_idx = np.argmax(correlation)
        lag = max_idx - (len(ref_approx) - 1)
        
        # Scale lag to original sampling rate
        scale_factor = window_size / len(ref_approx)
        scaled_lag = int(lag * scale_factor)
        
        return scaled_lag
        
    def apply_delay(self, delay_samples):
        """
        Apply delay to target signal to synchronize with reference
        
        Parameters:
        -----------
        delay_samples : int
            Delay to apply in samples
        
        Returns:
        --------
        sync_signal : array
            Synchronized target signal
        """
        # Limit delay to maximum value
        if abs(delay_samples) > self.max_delay:
            delay_samples = np.sign(delay_samples) * self.max_delay
            
        # Update current delay
        self.current_delay = delay_samples
        
        if delay_samples > 0:
            # Target signal is behind reference - shift forward
            self.sync_buffer = np.roll(self.target_buffer, delay_samples)
        else:
            # Target signal is ahead of reference - shift backward
            self.sync_buffer = np.roll(self.target_buffer, delay_samples)
            
        return self.sync_buffer[-self.fs:]  # Return latest 1 second
    
    def synchronize(self, method='wavelet'):
        """
        Perform full synchronization process
        
        Parameters:
        -----------
        method : str
            Method for phase detection ('crosscorrelation', 'hilbert', or 'wavelet')
            
        Returns:
        --------
        sync_signal : array
            Synchronized target signal
        phase_diff : float
            Detected phase difference in samples
        """
        # Detect phase difference
        if method == 'crosscorrelation':
            phase_diff = self.detect_phase_difference_crosscorrelation()
        elif method == 'hilbert':
            phase_diff = self.detect_phase_difference_hilbert()
        elif method == 'wavelet':
            phase_diff = self.detect_phase_difference_wavelet()
        else:
            raise ValueError(f"Unknown method: {method}")
            
        # Apply delay to synchronize
        sync_signal = self.apply_delay(phase_diff)
        
        return sync_signal, phase_diff
    
    def evaluate_synchronization(self):
        """
        Evaluate the quality of synchronization
        
        Returns:
        --------
        quality : float
            Synchronization quality (correlation coefficient)
        """
        # Get latest 1 second of data
        window = self.fs
        ref = self.reference_buffer[-window:]
        sync = self.sync_buffer[-window:]
        
        # Calculate correlation coefficient
        correlation = np.corrcoef(ref, sync)[0, 1]
        
        return correlation


# Example usage with simulated biosignals
def generate_ecg_like_signal(fs, duration, heart_rate=60, phase_shift=0):
    """
    Generate a simplified ECG-like signal
    
    Parameters:
    -----------
    fs : float
        Sampling frequency in Hz
    duration : float
        Signal duration in seconds
    heart_rate : float
        Heart rate in BPM
    phase_shift : float
        Phase shift in seconds
        
    Returns:
    --------
    signal : array
        Simulated ECG-like signal
    """
    t = np.arange(0, duration, 1/fs)
    
    # Basic frequency from heart rate
    freq = heart_rate / 60.0
    
    # Create QRS complex-like shape using gaussian pulses
    qrs_width = 0.1  # QRS width in seconds
    t_with_shift = t + phase_shift
    
    # Base signal with heartbeats
    signal = np.zeros_like(t)
    
    for i in range(int(duration * freq) + 1):
        beat_time = i / freq
        # QRS complex (R peak)
        signal += 1.0 * np.exp(-((t_with_shift - beat_time) ** 2) / (2 * (0.02 ** 2)))
        # Q wave
        signal -= 0.2 * np.exp(-((t_with_shift - beat_time + 0.05) ** 2) / (2 * (0.02 ** 2)))
        # S wave
        signal -= 0.3 * np.exp(-((t_with_shift - beat_time - 0.05) ** 2) / (2 * (0.02 ** 2)))
        # T wave
        signal += 0.3 * np.exp(-((t_with_shift - beat_time - 0.2) ** 2) / (2 * (0.08 ** 2)))
        # P wave
        signal += 0.15 * np.exp(-((t_with_shift - beat_time + 0.2) ** 2) / (2 * (0.05 ** 2)))
        
    # Add some noise
    noise = 0.05 * np.random.randn(len(t))
    signal = signal + noise
    
    return signal

def demonstrate_phase_sync():
    # Parameters
    fs = 1000  # Sampling frequency (Hz)
    duration = 10  # Signal duration (seconds)
    phase_shift = 0.2  # Phase shift (seconds)
    
    # Generate simulated ECG signals
    reference_signal = generate_ecg_like_signal(fs, duration, heart_rate=70, phase_shift=0)
    target_signal = generate_ecg_like_signal(fs, duration, heart_rate=70, phase_shift=phase_shift)
    
    # Add unique noise to each signal
    reference_signal += 0.03 * np.random.randn(len(reference_signal))
    target_signal += 0.03 * np.random.randn(len(target_signal))
    
    # Create phase synchronizer
    sync = PhaseSync(fs=fs)
    
    # Process in chunks to simulate real-time operation
    chunk_size = int(fs * 0.5)  # 500ms chunks
    num_chunks = int(duration * fs / chunk_size)
    
    # Storage for results
    phase_differences = []
    sync_quality = []
    
    # Run synchronization on chunks
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size
        
        ref_chunk = reference_signal[start_idx:end_idx]
        target_chunk = target_signal[start_idx:end_idx]
        
        # Update buffers
        sync.update_buffers(ref_chunk, target_chunk)
        
        # Only start synchronizing after initial buffer filling
        if i >= 2:
            # Synchronize signals
            sync_signal, phase_diff = sync.synchronize(method='wavelet')
            
            # Evaluate synchronization quality
            quality = sync.evaluate_synchronization()
            
            # Store results
            phase_differences.append(phase_diff)
            sync_quality.append(quality)
            
            # Print progress
            if i % 4 == 0:  # Print every 2 seconds
                print(f"Processing second {i*0.5:.1f}: Phase difference = {phase_diff} samples, Quality = {quality:.3f}")
    
    # Plot results
    plt.figure(figsize=(15, 10))
    
    # Plot final second of signals
    plt.subplot(3, 1, 1)
    t = np.arange(0, 1, 1/fs)
    plt.plot(t, reference_signal[-fs:], 'b-', label='Reference Signal')
    plt.plot(t, target_signal[-fs:], 'r-', label='Target Signal (Unsynchronized)')
    plt.title('Original Signals (Last Second)')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.plot(t, reference_signal[-fs:], 'b-', label='Reference Signal')
    plt.plot(t, sync.sync_buffer[-fs:], 'g-', label='Synchronized Signal')
    plt.title('Synchronized Signals (Last Second)')
    plt.legend()
    plt.grid(True)
    
    # Plot phase difference over time
    plt.subplot(3, 1, 3)
    chunks = np.arange(len(phase_differences)) * 0.5 + 1.0  # Time in seconds
    plt.plot(chunks, phase_differences, 'k-')
    plt.axhline(y=phase_shift*fs, color='r', linestyle='--', label=f'True Phase Shift ({phase_shift*fs} samples)')
    plt.title('Detected Phase Difference Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Phase Difference (samples)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    demonstrate_phase_sync()