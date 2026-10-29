// DC motor test through the L293D chip.
// Type in the Serial Monitor:  F = forward,  B = backward,  S = stop.
//
// Wiring (L293D, notch end = pins 1 and 16):
//   pin 1  (enable 1)  -> Uno 5     pin 16 (chip power) -> 5V
//   pin 2  (input 1)   -> Uno 7     pin 8  (motor power) -> 5V
//   pin 3  (output 1)  -> motor wire A
//   pin 4, 5 (ground)  -> GND
//   pin 6  (output 2)  -> motor wire B
//   pin 7  (input 2)   -> Uno 8

const int EN_PIN = 5;    // speed (PWM)
const int IN1_PIN = 7;   // direction
const int IN2_PIN = 8;   // direction
const int SPEED = 200;   // 0 (off) to 255 (full)

void drive(bool forward) {
  digitalWrite(IN1_PIN, forward ? HIGH : LOW);
  digitalWrite(IN2_PIN, forward ? LOW : HIGH);
  analogWrite(EN_PIN, SPEED);
}

void stopMotor() {
  analogWrite(EN_PIN, 0);
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
}

void setup() {
  Serial.begin(115200);
  pinMode(EN_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  stopMotor();
  Serial.println("Ready. Type F (forward), B (backward) or S (stop)");
}

void loop() {
  if (Serial.available()) {
    char c = toupper(Serial.read());
    if (c == 'F') { drive(true);  Serial.println("forward"); }
    if (c == 'B') { drive(false); Serial.println("backward"); }
    if (c == 'S') { stopMotor();  Serial.println("stop"); }
  }
}
