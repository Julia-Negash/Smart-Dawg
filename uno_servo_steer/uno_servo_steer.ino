// Step 1 of steering: the servo turns toward the note.
// Messages from the laptop over USB, same as uno_message_test:
//   <color>,<x>,<size>   e.g. P,-23,12     or   N  (nothing seen)
// x = -100 (far left) .. 100 (far right).
//
// Wiring (unloaded test): servo orange -> pin 9, red -> Uno 5V, brown -> Uno GND.

#include <Servo.h>

const int SERVO_PIN = 9;
const int CENTER = 90;        // servo angle for straight ahead
const int MAX_TURN = 40;      // furthest the servo turns either way (degrees)
const unsigned long TIMEOUT_MS = 1000;
const bool TYPING_TEST = false;  // true while typing messages by hand; set to false for the camera test

Servo steering;
char line[24];
byte len = 0;
unsigned long lastMsg = 0;

void handle(const char *msg) {
  lastMsg = millis();
  if (msg[0] == 'N') {
    steering.write(CENTER);
    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("nothing seen -> center");
    return;
  }
  char color;
  int x, size;
  if (sscanf(msg, "%c,%d,%d", &color, &x, &size) != 3) return;
  x = constrain(x, -100, 100);
  int angle = CENTER + (long)x * MAX_TURN / 100;   // left note -> smaller angle
  steering.write(angle);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.print(color);
  Serial.print("  x=");
  Serial.print(x);
  Serial.print("  -> servo ");
  Serial.println(angle);
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  steering.attach(SERVO_PIN);
  steering.write(CENTER);
  Serial.println("Ready. Send messages like P,-23,12 or N");
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      line[len] = '\0';
      if (len > 0) handle(line);
      len = 0;
    } else if (len < sizeof(line) - 1) {
      line[len++] = c;
    }
  }
  if (!TYPING_TEST && millis() - lastMsg > TIMEOUT_MS) {   // laptop went quiet: straighten out
    steering.write(CENTER);
    digitalWrite(LED_BUILTIN, LOW);
  }
}