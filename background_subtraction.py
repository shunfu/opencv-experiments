import numpy as np
import cv2

cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorMOG2(history=50,
										  varThreshold=36,
										  detectShadows=False)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    fgmask = fgbg.apply(frame)
    cv2.imshow('frame', fgmask)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()