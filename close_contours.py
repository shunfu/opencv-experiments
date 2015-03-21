import numpy as np
import cv2

def get_bounds(contours):
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
    return x_min, x_max, y_min, y_max

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
    cv2.fillPoly(frame, contours, (200, 200, 200)) # looks better

def draw_bounding_box(frame):
    # draw rect that holds the subject of the image
    fgmask = fgbg.apply(frame)
    _, contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.fillPoly(frame, contours, (0, 255, 0)) # looks better

    x_min, x_max, y_min, y_max = get_bounds(contours)
    # print "(%d : %d, %d : %d)"%(x_min, x_max, y_min, y_max)
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0))

def draw_canny_edge(frame):
    # draw canny edge of the subject of the image
    fgmask = fgbg.apply(frame)
    _, contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    x_min, x_max, y_min, y_max = get_bounds(contours)

    edges = cv2.Canny(frame, 100, 200)
    _, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    canny_frame = frame.copy()
    cv2.drawContours(canny_frame, contours, -1, (255, 255, 255), 1)
    frame[x_min:x_max,y_min:y_max] = canny_frame[x_min:x_max,y_min:y_max]
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 255, 255))

def draw_silhouette(frame):
    # draw silhouette of the subject
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, 0)
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.fillPoly(frame, contours, (0, 215, 25))

camera = cv2.VideoCapture(0)
# cv2.namedWindow('frame', cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
fgbg = cv2.createBackgroundSubtractorMOG2(history=50,
                                          varThreshold=36,
                                          detectShadows=False)

while True:
    # obtain and mirror the frame
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    # draw_full_contours(frame)
    # draw_subtracted_contours(frame)
    # draw_bounding_box(frame)
    # draw_canny_edge(frame)
    # draw_silhouette(frame)

    # fills in silhouette and then draws in forces
    draw_silhouette(frame)
    draw_subtracted_contours(frame)

    # display the frame
    cv2.imshow('frame', frame)

    # listen for esc key
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

camera.release()
cv2.destroyAllWindows()