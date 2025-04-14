# Phase Synchroniser Firmware

Arduino-based system for detecting and correcting phase differences between input signals.

## Description

The firmware dynamically detects and corrects phase differences between two input signals using digital potentiometers controlled via SPI.

## Features

- Zero-crossing detection for accurate phase measurement
- Real-time phase difference calculation
- Adaptive phase correction via digital potentiometers
- SPI communication for precise digital control

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
