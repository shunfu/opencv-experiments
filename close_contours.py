import numpy as np
import cv2

def draw_full_contours(frame):
    # draw contours on full image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, 0)
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

def draw_subtracted_contours(frame):
    # draw contours on background subtracted image
    fgmask = fgbg.apply(frame)
    _, contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame, contours, -1, (0, 255, 0), 20) # fills in full body shape
    cv2.fillPoly(frame, contours, (0, 255, 0)) # looks better

def draw_bounding_box(frame):
    # draw rect that holds the subject of the image

    fgmask = fgbg.apply(frame)
    _, contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.fillPoly(frame, contours, (0, 255, 0)) # looks better

    x_max = 0
    x_min = frame.shape[0]
    y_max = 0
    y_min = frame.shape[1]
    for cnt in contours:
        for coord in cnt:
            if coord[0][0] > x_max:
                x_max = coord[0][0]
            if coord[0][0] < x_min:
                x_min = coord[0][0]
            if coord[0][1] > y_max:
                y_max = coord[0][1]
            if coord[0][1] < y_min:
                y_min = coord[0][1]

    # print "(%d : %d, %d : %d)"%(x_min, x_max, y_min, y_max)
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0))

def draw_canny_edge(frame):
    # draw canny edge of the subject of the image
    pass

# TODO canny or contour of only the subject
# TODO fill it in!!

camera = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=50,
                                          varThreshold=36,
                                          detectShadows=False)

while True:
    # obtain and mirror the frame
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    # draw_full_contours(frame)
    # draw_subtracted_contours(frame)
    draw_bounding_box(frame)

    # display the frame
    cv2.imshow('frame', frame)


    # listen for esc key
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

camera.release()
cv2.destroyAllWindows()