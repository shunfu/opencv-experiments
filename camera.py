#!/usr/bin/env python
import numpy as np
import cv2

class Camera:
    def __init__(self, fullscreen=False):
        self.cam = cv2.VideoCapture(0)
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=50,
                                                       varThreshold=36,
                                                       detectShadows=False)
        if fullscreen:
            self.__setupCamera()
            self.__setupWindow()

    def __setupCamera(self):
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

    def __setupWindow(self):
        cv2.namedWindow('frame', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def update(self):
        ret, frame = self.cam.read()
        self.frame = cv2.flip(frame, 1)

    def get_and_draw_silhouette(self):
        # draw silhouette of the subject
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 127, 255, 0)
        _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.fillPoly(self.frame, contours, (0, 215, 25))
        return contours

    def get_forces_and_draw_subtracted_contours(self):
        # draw contours on background subtracted image
        fgmask = self.fgbg.apply(self.frame)
        _, contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(self.frame, contours, -1, (0, 255, 0), 20) # fills in full body shape
        cv2.fillPoly(self.frame, contours, (200, 200, 200)) # looks better
        return contours

    def display(self):
        cv2.imshow('frame', self.frame)

    def release(self):
        self.cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    camera = Camera(fullscreen=True)
    while True:
        camera.update()
        poly_contours = camera.get_and_draw_silhouette()
        forces_contours = camera.get_forces_and_draw_subtracted_contours()
        camera.display()
        if cv2.waitKey(1) == 27:
            break
    camera.release()