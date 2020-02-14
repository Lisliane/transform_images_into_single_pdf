""" Get max contour """

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>

# Third-party imports
import cv2
import numpy as np


class MaxContour:

    @staticmethod
    def apply(contours):
        """
            Get max contours of the image.
                where:
                    - contours: array of contours

                output:
                    - x, y, w, h: minimal up-right bounding rectangle for the specified point set.
        """

        # Find the index of the largest contour
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        x, y, w, h = cv2.boundingRect(contours[max_index])

        return x, y, w, h
