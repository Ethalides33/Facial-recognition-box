#include <Servo.h>
#include <LiquidCrystal.h>

Servo myservo; 
String inByte;
String msg;


// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
   // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("Initializing...");
  myservo.attach(9);
  Serial.begin(9600);
}

void loop()
{    
  lcd.setCursor(0, 0);
  if(Serial.available())  // if data available in serial port
    { 
    msg = Serial.readStringUntil('\n'); // read data until newline
    //msg = inByte.toInt();   // change datatype from string to integer
    Serial.println(msg);
    if (msg.endsWith("A")){ // recognized admin
      Serial.println("HERE!");
      myservo.write(0);
      lcd.print("Access granted.");
    }
    if (msg.endsWith("N")){
      Serial.println("NOTHERE!");
      myservo.write(110);
      lcd.print("Access denied.");
    }
    delay(1000); // in ms
    //Serial.print("Servo in position: ");  
    //Serial.println(inByte);
    }
}
