# Smart-Dawg 🐶🐾
Robotic dawg for our Mechanical Design Studio mini TopGolf competition, Dec 6 2026.
It uses a camera to find colored sticky notes on target boxes, drives to them,
and drops a ping pong ball into each box.
## How it works
- ESP32-CAM streams live video over WiFi
- Laptop runs OpenCV color detection on the stream and steers the robot
- Arduino Uno drives the wheel motors, ball-drop servo and ultrasonic sensor
