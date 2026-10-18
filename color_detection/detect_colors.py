import cv2
import numpy as np

# Your tuned numbers: name: (low, high, box color to draw)
COLORS = {
    "yellow": ([20, 150, 150], [35, 255, 255], (0, 255, 255)),
    "blue":   ([90, 80, 120], [112, 255, 255], (255, 0, 0)),
    "purple": ([125, 54, 138], [162, 255, 255], (255, 0, 255)),
}
MIN_AREA = 400   # ignore blobs smaller than this (specks of noise)


def find_notes(frame):
    """Return a list of (name, side, size, box) for each color it sees."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    width = frame.shape[1]
    found = []
    for name, (low, high, draw_color) in COLORS.items():
        mask = cv2.inRange(hsv, np.array(low), np.array(high))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            continue
        biggest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(biggest) < MIN_AREA:
            continue
        x, y, w, h = cv2.boundingRect(biggest)
        center_x = x + w // 2
        if center_x < width / 3:
            side = "LEFT"
        elif center_x > 2 * width / 3:
            side = "RIGHT"
        else:
            side = "CENTER"
        size = round(100 * w / width)   # % of the picture's width; bigger = closer
        found.append((name, side, size, (x, y, w, h)))
    return found


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    last = ""
    while True:
        ok, frame = cap.read()
        if not ok:
            print("No picture from the camera")
            break
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
        notes = find_notes(frame)

        for name, side, size, (x, y, w, h) in notes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), COLORS[name][2], 2)
            cv2.putText(frame, f"{name} {side} {size}%", (x, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLORS[name][2], 2)

        summary = ", ".join(f"{n} {s} {z}%" for n, s, z, _ in notes) or "nothing"
        if summary != last:          # only print when something changes
            print(summary)
            last = summary

        cv2.imshow("detect", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
