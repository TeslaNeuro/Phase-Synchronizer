# Phase Synchronizer

## Update
- Adding more to this repo so keep posted !
- Working on a rev.B ! I aim to create it for scalability and performance reasons !

## Project Overview
The Phase Synchronizer is a system designed to detect, synchronize, and adjust the phase of two arbitrary out of phase signals without modifying their frequency components. This project implements phase synchronization techniques to ensure that the relative phase between signals is maintained consistently, improving stability and performance in time-dependent systems such as neural signal processing of ENG/ECG bio-signals. The goal for this project is simplicity and cost-effectiveness, allowing quick hardware integration for various electronics engineers. The industry most commonly uses a PLL system to achieve this but the problem of PLLs are the use of oscillators which alter the signal frequency components down the chain making it difficult to process important data or information accurately.

## Typical considerations
It’s essential to maintain stability in the system after synchronization. Oscillations, noise, or disturbances can lead to drifting of the phase relationship, so a robust feedback mechanism may be needed to keep the signals synchronized over time.

## Key Features
- Phase Detection: Automatically identifies the phase difference between two signals.
- Phase Synchronization: Aligns the phase of the second signal with the first, ensuring phase lock.
- Phase Shift Correction: Adjusts any misaligned signals, resolving phase errors effectively. (In reality there will be uV-mV of noise floor still when Va + Vb is combined)
- Frequency Integrity: Maintains the frequency of both signals during synchronization.
- Closed-loop control: Continuously monitors and corrects phase shifts to maintain stable synchronization over time.

## Tools and Technologies
- Proteus: Used for simulating and analyzing the phase synchronization process for prototyping purposes.
- KiCAD: Used for designing the main circuit and sub-circuits, as well as BoM, PCB, Schematic and Mechanical drawings.
- Arduino IDE: Used for writing basic core embedded firmware and algorithms in C/C++ for simple microcontrollers.
- Analog Adjustable Filters: A core mechanism for frequency independent phase correction.
- Digital Signal Processing (DSP): For precise phase detection and control.

## How It Works
The system works by first detecting the phase difference between two incoming signals. A control loop then generates the necessary adjustments to bring the signals into phase alignment without changing their frequency. This is particularly useful for applications like communication systems, audio processing, biomedical ENG/ECG analysis, and time-sensitive data transmission.

Through precise time delay measurement and phase shift mapping, the system should ideally aleviate any delay errors. The process requires one signal to be phase compensated (Lead/Lag) at a time, this is highly imperative.

## Things to consider in your application

Not every implementation is perfect similar to other electronics circuits it needs to be optimised and further tested/improved to achieve desired outcomes.
- Stability, Crosstalk & Noise
- Signal Integrity
- Cost
- Space
- Reliability

At higher frequencies the system becomes less reliable and needs a complete re-design to achieve better phase correction. Thus a different approach and method may need to be considered as well. In essence phase compensation and accurate detection are two seperate things you will have to alter and re-define for better results.

## Applications
Communication Systems: Maintaining signal coherence in wireless and wired transmissions.
Audio Processing: Ensuring phase-aligned audio playback from multiple sources.
Signal Processing: Synchronizing clock signals in digital electronics for better data integrity.

## Example Proof of Concept PCB Prototype Rev.A
- As you can probably tell this is a very rushed modular pcb but still functional LOL!

![image](https://github.com/user-attachments/assets/e3681b8a-cc53-40aa-9b98-96b481a9995d)

## License

This project includes firmware, software, hardware designs, and integration components and is licensed under the [Custom License Agreement](./LICENSE).

- **Non-Commercial Use**: You may use, modify, and distribute this project for non-commercial purposes.
- **Commercial Use**: To use this project for commercial purposes, please contact the author at [arshiakeshvariasl@gmail.com] to obtain full permission rights and discuss licensing terms.

See the [LICENSE](./LICENSE) file for full licensing details.

## Additional Notes
Should you want to use/modify/edit/reference/get creative inspiration from it for commercial, corporate and company needs you must gain full permission of usage and discuss licensing from myself. Otherwise, Feel free to play around with the code to make it custom to your own requirements. 

Code can be improved for better error handling or detection !
You are welcome to contact me should you have any general and technical questions.
