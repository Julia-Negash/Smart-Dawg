import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cv2.namedWindow("sliders")
for name, start, top in [("H low", 20, 179), ("H high", 35, 179),
                         ("S low", 80, 255), ("S high", 255, 255),
                         ("V low", 120, 255), ("V high", 255, 255)]:
    cv2.createTrackbar(name, "sliders", start, top, lambda x: None)

while True:
    ok, frame = cap.read()
    if not ok:
        print("No picture from the camera")
        break
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    get = lambda n: cv2.getTrackbarPos(n, "sliders")
    low = np.array([get("H low"), get("S low"), get("V low")])
    high = np.array([get("H high"), get("S high"), get("V high")])
    mask = cv2.inRange(hsv, low, high)
    cv2.imshow("camera", frame)
    cv2.imshow("mask", mask)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("low =", low.tolist(), " high =", high.tolist())
        break

cap.release()
cv2.destroyAllWindows()
