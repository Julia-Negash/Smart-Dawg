// Wired test: the laptop sends messages like P,-23,12 over USB.
// The Uno says what the robot would do, and the built-in LED lights
// up while a note is seen. No motors yet.
//
// Message format:  <color>,<x>,<size>   or   N
//   color  Y, B or P
//   x      -100 (far left) .. 100 (far right)
//   size   note width as % of the picture (bigger = closer)
//   N      nothing seen

const unsigned long TIMEOUT_MS = 1000;  // no message for this long -> stop

char line[24];
byte len = 0;
unsigned long lastMsg = 0;
bool stopped = true;

void stopRobot(const char *why) {
  digitalWrite(LED_BUILTIN, LOW);
  if (!stopped) {
    Serial.print("STOP: ");
    Serial.println(why);
    stopped = true;
  }
}

void handle(const char *msg) {
  lastMsg = millis();
  if (msg[0] == 'N') {
    stopRobot("nothing seen");
    return;
  }
  char color;
  int x, size;
  if (sscanf(msg, "%c,%d,%d", &color, &x, &size) != 3 ||
      (color != 'Y' && color != 'B' && color != 'P')) {
    Serial.print("bad message: ");
    Serial.println(msg);
    return;
  }
  digitalWrite(LED_BUILTIN, HIGH);
  stopped = false;
  Serial.print(color);
  Serial.print("  x=");
  Serial.print(x);
  Serial.print("  size=");
  Serial.print(size);
  if (x < -20) Serial.println("  -> turn LEFT");
  else if (x > 20) Serial.println("  -> turn RIGHT");
  else Serial.println("  -> go STRAIGHT");
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
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
  if (millis() - lastMsg > TIMEOUT_MS) stopRobot("no messages from the laptop");
}

