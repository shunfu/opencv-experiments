import numpy as np
import cv2

camera = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=50,
                                          varThreshold=36,
                                          detectShadows=False)

while True:
    # obtain and mirror the frame
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    # isolate background, then find and draw contours
    fgmask = fgbg.apply(frame)
    ret, thresh = cv2.threshold(fgmask, 127, 255, 0)
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame, contours, -1, (0, 255, 0), 20) # fills in full body shape
    cv2.fillPoly(frame, contours, (0, 255, 0)) # looks better

    # display the frame
    cv2.imshow('frame', frame)

    # listen for esc key
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

camera.release()
cv2.destroyAllWindows()