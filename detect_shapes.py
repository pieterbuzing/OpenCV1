# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2

from rectangle import Rectangle
from rectangle_tree import Node


def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the input image")
    args = vars(ap.parse_args())

    # load the image and resize it to a smaller factor so that
    # the shapes can be approximated better
    image = cv2.imread(args["image"])
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])

    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    # gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (3, 3), 0.4)  # was (5, 5), 0
    # thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    # find contours in the thresholded image and initialize the
    # shape detector
    # cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # see https://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:100]

    print 'found %d contours' % len(cnts)

    root = Node(Rectangle(None, 0, 0, resized.shape[0], resized.shape[1]))

    for c in cnts:
        rect = detect(c)
        if rect is None:
            continue

        root.insert(rect)

        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")

        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

        cv2.imshow("Blurred", gray)
        cv2.imshow("Edged", edged)

        # show the output image
        cv2.imshow("Image", image)
        cv2.waitKey(0)

    node, count = root.findmaxchildren()
    board_rectangle = node.elem
    if board_rectangle.approx is None:
        print "No chess board found"
    else:
        c = board_rectangle.approx.astype("float")
        c *= ratio
        c = c.astype("int")

        cv2.drawContours(image, [c], -1, (255, 50, 0), 2)

        cv2.imshow("Image", image)
        cv2.waitKey(0)


def detect(c):
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

    # if the shape has 4 vertices, it is either a square or a rectangle
    if len(approx) != 4:
        return None

    rect = Rectangle(approx)

    return rect


if __name__ == "__main__":
    main()
