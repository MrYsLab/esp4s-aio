/*
  Esplora For Scratch/Snap!

Copyright (c) 2013-15 Alan Yorinks All rights reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU  General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


 This sketch is largely based upon the EsploraRemote sketch
 supplied as part of the Arduino Esplora Library within the Arduino IDE.
 */

#include <Esplora.h>
#define TINKERKIT_OUT_A 3
#define TINKERKIT_OUT_B 11
#define LED_PIN 13
#define dumpLoopTime 30  // 30 milliseconds
#define version "2.00"
#define ORIENTATION_LEFT    1
#define ORIENTATION_RIGHT   2
#define JOYSTICK_BUTTON 5

/* timer variables */
unsigned long currentMillis;        // store the current value from millis()
unsigned long previousMillis;       // for comparison with currentMillis
int samplingInterval = 25;          // how often to run the main loop (in ms)

boolean continuousDump = false;
int orientation = ORIENTATION_LEFT;  // joystick on left side of board
int temp_units = DEGREES_C;
int axis_data = 0;
int tempValue = 0;




void setup() {
  while (!Serial); // needed for Leonardo-based board like Esplora
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(TINKERKIT_OUT_A, OUTPUT);
  pinMode(TINKERKIT_OUT_B, OUTPUT);
  while( Serial.read() != -1)
    ;
}

void loop() {


  if (Serial.available()) {
    parseCommand();
  }
  if (continuousDump == true) {
    currentMillis = millis();
    if (currentMillis - previousMillis > samplingInterval) {
      previousMillis += samplingInterval;
      dumpInputs();
    }
  }
}

/*
 * This function reads a character from the serial line and
 * decide what to do next. The "what to do" part is given by
 * function it calls (e.g. dumpInputs(), setRed() and so on).
 */

/* COMMANDS
   Legacy Commands:
   Report all sensors      D
   Continuously Report     C
   Stop Continuous         S

   Red Led                 R
   Green Led               G
   Blue Led                B

   Board Led               L

   Set Tone                T

   Set TinkerKit A         J
   Set TinkerKit B         K

   Set Temp Units          U
   Set Orientation         O

*/

/* SENSOR STATUS REQUESTS
    Buttons:
        Switch 1 (Down)     a
        Switch 2( Left)     b
        Switch 3 (Up)       c
        Switch 4 (Right)    d

    Joystick
        Button              e
        x                   f
        y                   g

    Help                    h

    Light                   l

    Slider                  p

    Sound                   s

    Temperature             t

    TinkerKit
        A                   u
        B                   v


    Accelerometer
        x                   x
        y                   y
        z                   z

    Release Version         r

*/




void parseCommand() {
  char cmd = Serial.read();
  switch (cmd) {
    // commands - no reply provided
    // Legacy commands
    case 'D':
      dumpInputs(); // this is a one shot
      break;
    case 'C':
      dumpContinuous();
      break;
    case 'S':
      stopContinuous();
      break;

    // LED commands
    case 'R': // Red Led
      setRed();
      break;
    case 'G': // Green Led
      setGreen();
      break;
    case 'B': // Blue led
      setBlue();
      break;
    case 'L': // Board led
      setLed13();
      break ;
    case 'T': // User Specified Tone by Frequency
      setTone();
      break;
    case 'J': // set tinkerkit out channel a
      setTinkerKit1();
      break;
    case 'K': // set tinkerkit out channel b
      setTinkerKit2();
      break;
    case 'U': // set temperature units
      setTempUnits();
      break;
    case 'O': // set board orientation
      setOrientation();
      break;



    // commands with a reply - mainly to retrieve sensor values
    // buttons
    case 'a':
      correctButton(SWITCH_1);
      //Serial.println(Esplora.readButton(SWITCH_1));
      break;
    case 'b':
      correctButton(SWITCH_2);
      //Serial.println(Esplora.readButton(SWITCH_2));
      break;
    case 'c':
      correctButton(SWITCH_3);
      //Serial.println(Esplora.readButton(SWITCH_3));
      break;
    case 'd':
      correctButton(SWITCH_4);
      //Serial.println(Esplora.readButton(SWITCH_4));
      break;
    // joystick values
    case 'e': // joystick button
      correctButton(JOYSTICK_BUTTON);
      //Serial.println(Esplora.readJoystickSwitch());
      break;
    case 'f': // joystick x position
      correctAxis(Esplora.readJoystickX());
      break;
    case 'g': // joystick x position
      correctAxis(Esplora.readJoystickY());
      break;
    case 'h': // print help
      printHelp();
      break;
    case 'l': // light sensor
      Serial.println(Esplora.readLightSensor());
      break;
    case 'p': // slider - potentiometer
      //Serial.println(Esplora.readSlider());
      correctSlider();
      break;
    case 'r':
      getVersion();
      break;
    case 's': // sound level
      Serial.println(Esplora.readMicrophone());
      break;
    case 't': // temperature
      Serial.println(Esplora.readTemperature(temp_units));
      break;
    case 'u': // tinkerkit input A
      Serial.println(Esplora.readTinkerkitInputA());
      break;
    case 'v': // tinkerkit input B
      Serial.println(Esplora.readTinkerkitInputB());
      break;
    case 'x': // accelerometer X axis
      correctAxis(Esplora.readAccelerometer(X_AXIS));
      break;
    case 'y': // accelerometer Y axis
      correctAxis(Esplora.readAccelerometer(Y_AXIS));
      break;
    case 'z': // accelerometer Z axis
      correctAxis(Esplora.readAccelerometer(Z_AXIS));
      break;
  }
}


void dumpInputs() {
  Serial.print("ESP,");
  Serial.print(Esplora.readButton(SWITCH_1));
  Serial.print(',');
  Serial.print(Esplora.readButton(SWITCH_2));
  Serial.print(',');
  Serial.print(Esplora.readButton(SWITCH_3));
  Serial.print(',');
  Serial.print(Esplora.readButton(SWITCH_4));
  Serial.print(',');
  Serial.print(Esplora.readSlider());
  Serial.print(',');
  Serial.print(Esplora.readLightSensor());
  Serial.print(',');
  Serial.print(Esplora.readTemperature(DEGREES_C));
  Serial.print(',');
  Serial.print(Esplora.readMicrophone());
  Serial.print(',');
  Serial.print(Esplora.readJoystickSwitch());
  Serial.print(',');
  Serial.print(Esplora.readJoystickX());
  Serial.print(',');
  Serial.print(Esplora.readJoystickY());
  Serial.print(',');
  Serial.print(Esplora.readAccelerometer(X_AXIS));
  Serial.print(',');
  Serial.print(Esplora.readAccelerometer(Y_AXIS));
  Serial.print(',');
  Serial.print(Esplora.readAccelerometer(Z_AXIS));
  Serial.print(',');
  Serial.print(Esplora.readTinkerkitInputA());
  Serial.print(',');
  Serial.print(Esplora.readTinkerkitInputB());
  Serial.print(',');
  Serial.print("PSE");
  Serial.println();

}

void setTempUnits() {
  temp_units = Serial.parseInt();
}

void setOrientation() {
  orientation = Serial.parseInt();
}

void setRed() {
  Esplora.writeRed(Serial.parseInt());
}

void setGreen() {
  Esplora.writeGreen(Serial.parseInt());
}

void setBlue() {
  Esplora.writeBlue(Serial.parseInt());
}

void setTone() {
  Esplora.tone(Serial.parseInt());
}

void setLed13() {
  int ledState = Serial.parseInt();
  if ( ledState != 0 )
  {
    ledState = 1;
  }
  digitalWrite(LED_PIN, ledState);
}

void setTinkerKit1() {
  analogWrite(TINKERKIT_OUT_A, Serial.parseInt());
}

void setTinkerKit2() {
  analogWrite(TINKERKIT_OUT_B, Serial.parseInt());
}



void getVersion() {
  Serial.println(version);
}

void dumpContinuous() {
  continuousDump = true;
}

void stopContinuous() {
  continuousDump = false;
}

void printHelp() {
  Serial.println("Set Board (L13) Led state: L0 to turn OFF and L1 to turn ON");
  Serial.println("Set LED Value: LED Value where LED is R for read, G for green and B for blue. Example: R100");
}
/* COMMANDS
 Legacy Commands:
 Report all sensors      D
 Continuously Report     C
 Stop Continuous         S

 Red Led                 R
 Green Led               G
 Blue Led                B

 Board Led               L

 Set Tone                T

 Set TinkerKit A         J
 Set TinkerKit B         K

 Set Temp Units          U
 Set Orientation         O



SENSOR STATUS REQUESTS
  Buttons:
      Switch 1 (Down)     a
      Switch 2( Left)     b
      Switch 3 (Up)       c
      Switch 4 (Right)    d

  Joystick
      Button              e
      x                   f
      y                   g

  Help                    h

  Light                   l

  Slider                  p

  Sound                   s

  Temperature             t

  TinkerKit
      A                   u
      B                   v


  Accelerometer
      x                   x
      y                   y
      z                   z

  Release Version         r
Serial.println('Not Yet Implemented'); */



void correctButton(int button)
{
  tempValue = Esplora.readButton(button);
  if ( button == JOYSTICK_BUTTON) {
    tempValue = Esplora.readJoystickSwitch();
  }
  else {
    tempValue = Esplora.readButton(button);
  }

  if ( tempValue == 0) {
    Serial.println("1");
  }
  else {
    Serial.println("0");
  }
}

void correctSlider() {
  tempValue = Esplora.readSlider();
  if (orientation == ORIENTATION_LEFT) {
    tempValue = abs(1023 - tempValue);
  }
  Serial.println(tempValue);
}

void correctAxis(int data) {
  if (orientation == ORIENTATION_LEFT) {
    data *= -1;
  }
  Serial.println(data);
}


