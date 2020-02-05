"""
    Auto crop
"""

# Third-party imports
import cv2

# Own imports
from utils.base import BaseClass


class Crop(BaseClass):

    def crop(self, image, boundaries):
        """
            Crop image

            Parameters:
                - image: array of image
                - boundaries:

            Returns:
                -
        """

        x_min, y_min, x_max, y_max = boundaries

        return image[y_min:y_max, x_min:x_max]

    def get_bounding_rectangle(self, image):
        """
            Get contours of the image

            Parameters:
                - image: array of image

            Returns:
                - size_total: integer containing the total image size
        """

        _, thresh = cv2.threshold(image, int(0.5 * 255), 255, cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        maxarea = 0
        cnt = None

        for h, tcnt in enumerate(contours):
            area = cv2.contourArea(tcnt)
            if area > maxarea:
                maxarea = area
                cnt = tcnt

        (x, y, w, h) = (0, 0, 0, 0)
        if cnt is not None:
            x, y, w, h = cv2.boundingRect(cnt)

        return x, y, w, h

    def apply(self, image):
        """
            Crop image
        """

        self.message.toprint('IMAGE_CROP')

        bounds = self.get_bounding_rectangle(image)
        image_cropped = self.crop(image, bounds)
        image_out = image_cropped

        self.message.toprint('IMAGE_CROPED')

        return image_out
