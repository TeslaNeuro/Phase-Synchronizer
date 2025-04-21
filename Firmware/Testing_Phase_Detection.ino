#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x20,20,4);  // changed to 0x27 due to lcd issues
int pulse_A = 7;
int pulse_B = 6;
int Tx_A,Tx_B,duty,Tx_A_LOW,Tx_B_LOW;
float freq_A,freq_B,period_A,period_B;
   
void setup()
{
  pinMode(pulse_A,INPUT);
  pinMode(pulse_B,INPUT);
  lcd.begin(16, 4);
  lcd.clear();
  lcd.print("Freq A:");
  lcd.setCursor(0,1);
  lcd.print("Tx A:");
  lcd.setCursor(0,2);
  lcd.print("Tx B:");  
  lcd.setCursor(0,3);
  lcd.print("Freq B:");  
}
void loop()
{
   Tx_A = pulseIn(pulse_A,HIGH);
   Tx_A_LOW = pulseIn(pulse_A,LOW);
   Tx_B = pulseIn(pulse_B,HIGH);
   Tx_B_LOW = pulseIn(pulse_B,LOW);
   period_A = Tx_A + Tx_A_LOW;
   period_B = Tx_B + Tx_B_LOW;
   freq_A = 1000000.0/period_A;
   freq_B = 1000000.0/period_B;
   //duty = (ontime/period)*100; 
   lcd.setCursor(6,1);
   lcd.print(Tx_A);
   lcd.print("us");
   lcd.setCursor(6,2);
   lcd.print(Tx_B); 
   lcd.print("us");   
   lcd.setCursor(7,0); 
   lcd.print(freq_A);
   lcd.print("Hz");
   lcd.setCursor(7,3);
   lcd.print(freq_B); 
   lcd.print("Hz"); 
}
