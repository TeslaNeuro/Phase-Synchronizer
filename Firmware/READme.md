# Phase Synchroniser

Arduino-based system for detecting and correcting phase differences between input signals.

## Description

The firmware dynamically detects and corrects phase differences between two input signals using digital potentiometers controlled via SPI.

## Features

- Zero-crossing detection for accurate phase measurement
- Real-time phase difference calculation
- Adaptive phase correction via digital potentiometers
- SPI communication for precise digital control

## Hardware Requirements

- Arduino board
- Digital potentiometer with SPI interface
- Two signal inputs (1000Hz reference frequency)
- SPI-compatible connections

## Installation

1. Connect digital potentiometers to SPI pins and CS pins (10 and 9)
2. Connect signal inputs to pins 7 and 6
3. Upload the code to your Arduino

## Usage

The system automatically:
1. Detects zero-crossing points
2. Calculates phase differences
3. Applies corrections via the digital potentiometers
4. Continuously monitors in a feedback loop

## Pin Configuration

```
CS_pin_1 (10): Chip select for signal A potentiometer
CS_pin_2 (9):  Chip select for signal B potentiometer
pulse_A (7):   Input pin for signal A
pulse_B (6):   Input pin for signal B
```

## Limitations

- Optimized for small phase corrections (0-5 degrees)
- Tuned for 1000Hz signals (adjustable in code)

## License

Custom License Protected - All rights reserved by Arshia Keshvari

## Author

**Arshia Keshvari**
