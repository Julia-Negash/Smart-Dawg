import threading
import cv2
import numpy as np
 
STREAM_URL = "http://172.20.10.6:81/stream"
 
# Your tuned numbers: name: (low, high, box color to draw)
COLORS = {
    "yellow": ([17, 80, 120], [35, 255, 255], (0, 255, 255)),
    "blue":   ([84, 35, 111], [101, 255, 255], (255, 0, 0)),
    "purple": ([124, 21, 96], [150, 255, 255], (255, 0, 255)),
}
MIN_AREA = 150      # ignore blobs smaller than this (specks of noise)
MIN_FILL = 0.6      # how solid the blob is (1.0 = a perfect filled rectangle)
MAX_STRETCH = 2.5   # a note is roughly square; reject long thin strips
FRAMES_NEEDED = 4   # must be seen this many frames in a row before it counts
KERNEL = np.ones((5, 5), np.uint8)
 
 
class Camera:
    """Keeps reading the stream in the background so we always use the newest frame."""
 
    def __init__(self, url):
        self.cap = cv2.VideoCapture(url)
        self.frame = None
        self.running = True
        threading.Thread(target=self._read, daemon=True).start()
 
    def _read(self):
        while self.running:
            ok, frame = self.cap.read()
            if ok:
                self.frame = frame
 
    def latest(self):
        return self.frame
 
 
def find_notes(frame):
    """Return {name: (side, size, box)} for each color that looks like a sticky note."""
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)          # smooth out camera noise
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    width = frame.shape[1]
    found = {}
    for name, (low, high, draw_color) in COLORS.items():
        mask = cv2.inRange(hsv, np.array(low), np.array(high))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL)   # remove specks
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL)  # fill small holes
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in sorted(contours, key=cv2.contourArea, reverse=True):
            area = cv2.contourArea(c)
            if area < MIN_AREA:
                break
            x, y, w, h = cv2.boundingRect(c)
            fill = area / (w * h)
            stretch = max(w, h) / min(w, h)
            if fill < MIN_FILL or stretch > MAX_STRETCH:
                continue                                    # wrong shape, try the next blob
            center_x = x + w // 2
            if center_x < width / 3:
                side = "LEFT"
            elif center_x > 2 * width / 3:
                side = "RIGHT"
            else:
                side = "CENTER"
            size = round(100 * w / width)   # % of the picture's width; bigger = closer
            found[name] = (side, size, (x, y, w, h))
            break
    return found
 
 
if __name__ == "__main__":
    cam = Camera(STREAM_URL)
    streak = {name: 0 for name in COLORS}   # frames in a row each color was seen
    last = ""
    while True:
        frame = cam.latest()
        if frame is None:
            if cv2.waitKey(50) & 0xFF == ord("q"):
                break
            continue
        frame = frame.copy()
        notes = find_notes(frame)
 
        steady = []
        for name in COLORS:
            streak[name] = streak[name] + 1 if name in notes else 0
            if streak[name] >= FRAMES_NEEDED:
                side, size, (x, y, w, h) = notes[name]
                steady.append(f"{name} {side} {size}%")
                cv2.rectangle(frame, (x, y), (x + w, y + h), COLORS[name][2], 2)
                cv2.putText(frame, f"{name} {side} {size}%", (x, max(12, y - 6)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLORS[name][2], 1)
 
        summary = ", ".join(steady) or "nothing"
        if summary != last:          # only print when something changes
            print(summary)
            last = summary
 
        cv2.imshow("detect", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
 
    cam.running = False
    cv2.destroyAllWindows()
