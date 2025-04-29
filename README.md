# Phase Synchronizer

## Update
- I’m adding more to this repo, stay tuned!
- The existing code is a simplified proof-of-concept and may require adjustments. Use at your discretion.
- Working on Rev. B! It will focus on scalability and performance.
- Goal: robust enough to handle worst-case scenarios.

## Project Overview
The **Phase Synchronizer** detects, synchronizes, and adjusts the phase of two arbitrary out-of-phase signals without altering their frequency. This ensures consistent relative phase alignment, improving stability and performance in time-dependent systems like ENG/ECG signal processing.

Traditional PLL systems alter signal frequency due to oscillators. This project aims to offer a simple, cost-effective alternative for easier hardware integration.

## Typical Considerations
After synchronization, system stability is key. Noise or disturbances can cause drift, so a robust feedback mechanism is recommended. FIFO (First-In-First-Out) architectures can deliver excellent results.

## Key Features
- **Phase Detection**: Identifies phase differences automatically.
- **Phase Synchronization**: Aligns signal phases with precision.
- **Phase Shift Correction**: Resolves misalignments effectively (some µV–mV noise floor may remain).
- **Frequency Integrity**: Original frequencies are preserved.
- **Closed-loop Control**: Continuously monitors and corrects phase shifts.

## Tools and Technologies
- **Proteus**: Simulation and analysis.
- **KiCAD**: Circuit design, BoM, PCB, schematics, mechanical drawings.
- **Arduino IDE**: Firmware development in C/C++.
- **Analog Adjustable Filters**: Frequency-independent phase correction.
- **DSP**: Accurate phase detection and control.

## How It Works
The system:
1. Detects phase difference between two signals.
2. Adjusts one to align with the other—without changing frequency.
3. Applies to telecom, audio, biomedical, and timing-sensitive systems.

*Only one signal should be phase-compensated (lead/lag) at a time.*

<img src="https://github.com/user-attachments/assets/9f18a7c6-bf8b-4e75-bf1f-e3aac7fbcd86" width="350x350">

<img src="https://github.com/user-attachments/assets/bac17197-6d40-4e15-acd5-1145ced28a75" width="500x500">

<img src="https://github.com/user-attachments/assets/c3e8beb6-9ef1-4e9c-9389-79d385159a9f" width="500x500">

## Implementation Considerations
No design is perfect; ongoing optimization is essential. Consider:
- Stability, crosstalk, noise
- Signal integrity
- Cost, space
- Long-term reliability

At high frequencies, the current setup is less effective. A redesign may be necessary. Note: both input signals must have the same frequency and amplitude.

**Tip:** Model the system in MATLAB before hardware implementation.

## Applications
- **Telecom**: Signal coherence in wireless/wired transmission.
- **Audio**: Phase-aligned multi-source playback.
- **Digital Systems**: Synchronized clocks for data accuracy.

## Proof of Concept – Rev. A PCB
- My first (rushed!) modular PCB from 2022 ! still functional.
- Used BNC connectors, tested with low-frequency signals (~100 Hz).
- You may need a signal generator or oscilloscope with phase-shift function. Filters (passive/active) can help too.

![Prototype Image](https://github.com/user-attachments/assets/e3681b8a-cc53-40aa-9b98-96b481a9995d)

## License
This project includes firmware, software, hardware designs, and integration components.

- **Non-Commercial Use**: Free to use, modify, and distribute.
- **Commercial Use**: Contact [arshiakeshvariasl@gmail.com](mailto:arshiakeshvariasl@gmail.com) for permission and licensing.

See [LICENSE](./LICENSE) for full details.

## Additional Notes
Want to use, modify, or take inspiration from this for commercial/corporate use? Please get in touch for licensing.

Feel free to tweak the code to fit your needs, there’s room to improve error handling and detection.

**Contact**: For general or technical questions, I’m happy to help!
