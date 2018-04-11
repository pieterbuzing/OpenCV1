import cv2


class Rectangle:
    def __init__(self, approx=None, x=0, y=0, w=0, h=0):
        if approx is not None:
            (x, y, w, h) = cv2.boundingRect(approx)
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.approx = approx

    def contains(self, small):
        fit_horizontal = self.x < small.x and self.x + self.width > small.x + small.width
        fit_vertical = self.y < small.y and self.y + self.height > small.y + small.height
        return fit_horizontal and fit_vertical
