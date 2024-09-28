/*
    Basic Code to test Phase Synchroniser Rev.A Prototype
    Author: Arshia Keshvari
    Date: 09/28/2024
    Custom License Protected
*/

#include <SPI.h>

const int CS_pin_1 = 10; // Chip select pin for signal A
const int CS_pin_2 = 9;  // Chip select pin for signal B
const int pulse_A = 7;   // Input pin for signal A
const int pulse_B = 6;   // Input pin for signal B
const float signalFrequency = 1000.0; // Frequency of the input signals in Hz
const float period = 1000000.0 / signalFrequency; // Period of the signal in microseconds
const int potAddress = 0x11; // Digital potentiometer address

// Initialize SPI communication
void setup() {
    pinMode(CS_pin_1, OUTPUT);
    pinMode(CS_pin_2, OUTPUT);
    SPI.begin();
    pinMode(pulse_A, INPUT);
    pinMode(pulse_B, INPUT);
}

// Measure the duration of the HIGH pulse for zero-crossing detection
unsigned long MeasureZeroCrossingDelay(int pulsePin) {
    unsigned long startTime = micros();
    while (digitalRead(pulsePin) == LOW);
    unsigned long highStart = micros();
    while (digitalRead(pulsePin) == HIGH);
    unsigned long highEnd = micros();
    return highEnd - highStart; // Duration of the HIGH pulse
}

// Calculate the phase error between the two signals
float CalculatePhaseError(int delayA, int delayB) {
    return (delayA - delayB) * (360.0 / period); // Convert delay difference to phase difference in degrees
}

// Write to the digital potentiometer
void DigitalPotWrite(int CS_Pin, int value) {
    digitalWrite(CS_Pin, LOW);
    SPI.transfer(potAddress);
    SPI.transfer(value);
    digitalWrite(CS_Pin, HIGH);
}

// Map phase shift to digital potentiometer value
int MapPhaseShiftToPotValue(float phaseShift) {
    int potValue = 255; // Default value for no phase shift
    if (phaseShift >= 0 && phaseShift <= 5) { // Adjust according to your required range
        potValue = map(phaseShift, 0, 5, 255, 0); // Map 0 to 5 degrees to pot value
    }
    return constrain(potValue, 0, 255); // Ensure potValue is within valid range
}

// Apply phase shift based on calculated error
void ApplyPhaseShift(float requiredShift) {
    int potValue = MapPhaseShiftToPotValue(requiredShift); // Convert phase shift to pot value
    DigitalPotWrite(CS_pin_1, potValue); // Apply phase shift to signal A
}

// Adaptive phase adjustment function
void AdaptivePhaseAdjustment() {
    int delayA = MeasureZeroCrossingDelay(pulse_A); // Measure delay for signal A
    int delayB = MeasureZeroCrossingDelay(pulse_B); // Measure delay for signal B
    
    float phaseError = CalculatePhaseError(delayA, delayB); // Calculate phase error
    ApplyPhaseShift(phaseError); // Adjust phase shift based on error
}

// Main loop
void loop() {
    AdaptivePhaseAdjustment(); // Continuously adjust phase based on real-time measurement
    delay(50); // Adjust for system performance
}
