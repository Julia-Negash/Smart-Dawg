# Wired test, part 2: find the target note with the ESP32-CAM and send
# messages like P,-23,12 to the Uno over USB about 10 times a second.
# Needs detect_colors.py in the same folder.
import time
import cv2
import serial
from detect_colors import Camera, find_notes, COLORS, FRAMES_NEEDED, STREAM_URL

UNO_PORT = "/dev/cu.usbmodem101"   # the Uno's port (shown at the top of the Serial Monitor)
TARGET = "purple"                   # which note to drive toward: yellow, blue or purple
SEND_EVERY = 0.1                    # seconds between messages (10 per second)
LETTER = {"yellow": "Y", "blue": "B", "purple": "P"}


def make_message(notes, width):
    """Turn what the camera sees into a message like P,-23,12 (or N for nothing)."""
    if TARGET not in notes:
        return "N"
    side, size, (x, y, w, h) = notes[TARGET]
    center_x = x + w / 2
    offset = round((center_x - width / 2) / (width / 2) * 100)   # -100 left .. 100 right
    return f"{LETTER[TARGET]},{offset},{size}"


if __name__ == "__main__":
    uno = serial.Serial(UNO_PORT, 115200, timeout=0)
    time.sleep(3)                       # the Uno restarts when the port opens; give it a moment
    cam = Camera(STREAM_URL)
    streak = 0
    last_send = 0
    while True:
        frame = cam.latest()
        if frame is not None:
            frame = frame.copy()
            notes = find_notes(frame)
            streak = streak + 1 if TARGET in notes else 0
            if streak < FRAMES_NEEDED:      # not steady yet: treat as not seen
                notes.pop(TARGET, None)
            msg = make_message(notes, frame.shape[1])

            if time.time() - last_send >= SEND_EVERY:
                uno.write((msg + "\n").encode())
                last_send = time.time()

            if TARGET in notes:
                x, y, w, h = notes[TARGET][2]
                cv2.rectangle(frame, (x, y), (x + w, y + h), COLORS[TARGET][2], 2)
            cv2.putText(frame, "sending " + msg, (5, 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
            cv2.imshow("send to uno", frame)

        reply = uno.read(200).decode(errors="ignore")   # show what the Uno says back
        if reply:
            print(reply, end="")

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    uno.write(b"N\n")                   # leave the robot stopped
    cam.running = False
    uno.close()
    cv2.destroyAllWindows()
