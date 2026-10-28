// Ball dropper test: type D in the Serial Monitor and the coil turns exactly once (360 degrees).
//
// Wiring: 28BYJ-48 white plug -> ULN2003 board socket.
//         ULN2003 IN1 -> A0, IN2 -> A1, IN3 -> A2, IN4 -> A3.
//         ULN2003 + -> Uno 5V, - -> Uno GND.

#include <Stepper.h>

const int STEPS_PER_TURN = 2048;  // 28BYJ-48: 2048 steps = one full turn
const int SPEED_RPM = 12;         // 28BYJ-48 tops out around 15
const int DIRECTION = 1;          // change to -1 if the coil turns the wrong way

// The Stepper library wants the pins in the order IN1, IN3, IN2, IN4 for this motor.
Stepper coil(STEPS_PER_TURN, A0, A2, A1, A3);

void release() {  // turn the coils off between drops so the motor doesn't get hot
  digitalWrite(A0, LOW);
  digitalWrite(A1, LOW);
  digitalWrite(A2, LOW);
  digitalWrite(A3, LOW);
}

void dropBall() {
  Serial.println("Turning...");
  coil.step(DIRECTION * STEPS_PER_TURN);
  release();
  Serial.println("Done, one turn");
}

void setup() {
  Serial.begin(115200);
  coil.setSpeed(SPEED_RPM);
  release();
  Serial.println("Ready. Type D to drop one ball");
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'D' || c == 'd') dropBall();
  }
}
