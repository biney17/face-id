/*
  ========================================
  ARDUINO - Servo Control via Serial
  Face ID Door Controller
  
  Wiring:
    - Servo Signal → Pin 9
    - Servo VCC    → 5V
    - Servo GND    → GND
  
  Received Commands:
    'O' → Open the door (servo 90°)
    'C' → Close the door (servo 0°)
    
  Sent Status:
    'O' → Door is OPEN
    'F' → Door is CLOSED
  ========================================
*/

#include <Servo.h>

Servo doorServo;

const int SERVO_PIN = 9;
const int OPEN_ANGLE = 90;    // Angle for open door
const int CLOSE_ANGLE = 0;     // Angle for closed door

char doorStatus = 'F';  // Track current door status (F = Fermé/Closed, O = Open)

void setup() {
  Serial.begin(9600);
  doorServo.attach(SERVO_PIN);
  doorServo.write(CLOSE_ANGLE);  // Initial position: closed
  delay(500);
  Serial.println("Arduino Face ID Door - Ready");
  Serial.println("F");  // Send initial status
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == 'O') {
      doorServo.write(OPEN_ANGLE);
      delay(500);  // Wait for servo to move
      if (doorStatus != 'O') {
        doorStatus = 'O';
        Serial.println("O");  // Send status: OPEN
        Serial.println("DOOR OPENED");
      }
    }
    else if (command == 'C' || command == 'F') {
      doorServo.write(CLOSE_ANGLE);
      delay(500);  // Wait for servo to move
      if (doorStatus != 'F') {
        doorStatus = 'F';
        Serial.println("F");  // Send status: FERMÉ/CLOSED
        Serial.println("DOOR CLOSED");
      }
    }
  }
}