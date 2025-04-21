// OG Phase synchronizer
// Author: Arshia Keshvari
// Used actual mathematics, pen and paper for this
// Date: 19/02/2022

/*
  Uno            MCP41010    10k ohm digital pot resistor
   -------------------------
   D10           CS  (pin 1)
   D11 (MOSI)    SI  (pin 3)
   D13 (SCK)     SCK (pin 2)
*/

/*
  Uno            MCP41010    10k ohm digital pot resistor
   -------------------------
   D9            CS  (pin 1)
   D11 (MOSI)    SI  (pin 3)
   D13 (SCK)     SCK (pin 2)
*/

#include <SPI.h>                   // Serial Peripheral interface library used for serial communication between arduino and the SPI supported hardware

int CS_pin_1= 10;                  // Chip select pin 10 is for signal A if it contains a delay at 5 ms
int CS_pin_2= 9;                   // Chip select pin 9 is for signal B if it contains a delay at 5 ms
const int  maxPositions = 256;     // wiper can move from 0 to 255 = 256 positions
const byte pot_address = 0x11;     // Digital potentiometer address (For both digi pots its the same address)

bool Do_We_Have_A_Signal_Yet = false;              // this bool is to check if we have a signal yet
char Which_Signal_Are_We_Putting_The_Shift = 'N';  //if char 'a' then signal a, if char 'b' then to signal b, and N for null

int pulse_A = 7;    // Signal pulse A
int pulse_B = 6;    // Signal pulse B
int Tx_A,Tx_B;      // Time delay for A and B


int Delay_A_Getter(){
  Tx_A = pulseIn(pulse_A,HIGH);
 
  return Tx_A;
}


int Delay_B_Getter(){
   Tx_B = pulseIn(pulse_B,HIGH);
   
   return Tx_B;
}


// Digital potentiometer SPI communication
void Digital_PotWrtie(int CS_Pin, int value){
  digitalWrite(CS_Pin, LOW);
  SPI.transfer(pot_address);
  SPI.transfer(value);
  digitalWrite(CS_Pin, HIGH);
  }


// Returns a phase shift value from the corresponding time delay value
float ReturnDegreePhaseShift_FromTime(int uS_time){
  if (uS_time >= 133 and uS_time <=140){return 5;}
  else if (uS_time >= 119 and uS_time <=126){return 4.5;}
  else if (uS_time >= 105 and uS_time <=112){return 4;}
  else if (uS_time >= 91 and uS_time <=98){return 3.5;}
  else if (uS_time >= 78 and uS_time <=84){return 3;}
  else if (uS_time >= 64 and uS_time <=70){return 2.5;}
  else if (uS_time >= 50 and uS_time <=56){return 2;}
  else if (uS_time >= 36 and uS_time <=42){return 1.5;}
  else if (uS_time >= 22 and uS_time <=29){return 1;}
  else if (uS_time >= 14 and uS_time <=15){return 0.5;}
  else {return 0;}
}


// Phase shift resistance allocation
void PhaseShifting (int CS_Pin, float angle_phase_shift_required){
  int Digital_Resistance;
  if (angle_phase_shift_required == 0){Digital_Resistance = 255;}
  else if (angle_phase_shift_required == 0.5){Digital_Resistance = 231;}
  else if (angle_phase_shift_required == 1){Digital_Resistance = 206;}
  else if (angle_phase_shift_required == 1.5){Digital_Resistance = 180;}
  else if(angle_phase_shift_required == 2){Digital_Resistance = 153;}
  else if (angle_phase_shift_required == 2.5){Digital_Resistance = 127;}
  else if(angle_phase_shift_required == 3){Digital_Resistance = 101;}
  else if (angle_phase_shift_required == 3.5){Digital_Resistance = 75;}
  else if(angle_phase_shift_required == 4){Digital_Resistance = 50;}
  else if (angle_phase_shift_required == 4.5){Digital_Resistance = 25;}
  else if(angle_phase_shift_required == 5){Digital_Resistance = 0;}
  
  Digital_PotWrtie(CS_Pin, Digital_Resistance);
  }


/*
 *int 1 = 206  <- for 1 degree phase shift
 *int 2 = 153  <- for 2 degree phase shift
 *int 3 = 101  <- for 3 degree phase shift
 *int 4 = 50   <- for 4 degree phase shift
 *int 5 = 0    <- for 5 degree phase shift
*/


// Phase polarity conditioning
char checking_which_signal_comes_first(){
  
  while (true){
    if (digitalRead(pulse_A) == HIGH and Do_We_Have_A_Signal_Yet == false){Do_We_Have_A_Signal_Yet = true; return 'a';}      
    if (digitalRead(pulse_B) == HIGH and Do_We_Have_A_Signal_Yet == false){Do_We_Have_A_Signal_Yet = true; return 'b';}
    }
    
  }


// Applies the correct phase shift to the phase shifter or signal of interest
void Algo(){

  float PhaseShiftAngleForSignal;
  int Signal_delay;
  char Signal_we_are_proccessing;
  
  if (Do_We_Have_A_Signal_Yet == false){
    Signal_we_are_proccessing = checking_which_signal_comes_first();
    }
  
  if (Do_We_Have_A_Signal_Yet == true){
    // if statment to work with signal a
    if (Signal_we_are_proccessing == 'a'){
      Signal_delay = Delay_A_Getter();    // gets the us delay for signal a
      PhaseShiftAngleForSignal = ReturnDegreePhaseShift_FromTime(Signal_delay);   //calculates the phaseshift angle for the time delay
      
      Digital_PotWrtie(CS_pin_2, 255);  //turn off pot for signal b
  
      PhaseShifting(CS_pin_1, PhaseShiftAngleForSignal);    //writes to pot_a
  
      }
  
    // if statment to work with signal b
    else if (Signal_we_are_proccessing == 'b'){
      Signal_delay = Delay_B_Getter();    // gets the us delay for signal b
      PhaseShiftAngleForSignal = ReturnDegreePhaseShift_FromTime(Signal_delay);   //calculates the phaseshift angle for the time delay
      
      Digital_PotWrtie(CS_pin_1, 255);   //turn off pot for signal a
      
      PhaseShifting(CS_pin_2, PhaseShiftAngleForSignal);    //writes to pot_b
      }
    }
    

  
  }



void setup()
{
  pinMode(CS_pin_1, OUTPUT);
  pinMode(CS_pin_2, OUTPUT);
  SPI.begin();
  
  pinMode(pulse_A,INPUT);
  pinMode(pulse_B,INPUT);
}

void loop(){Algo();}
