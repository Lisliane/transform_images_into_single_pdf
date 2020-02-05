"""
    Converts image to grayscale
"""

# Third-party imports
import cv2

# Own imports
from utils.base import BaseClass


class ConvertToGray(BaseClass):

    def apply(self, image):
        """
            Converts image to grayscale
        """

        self.message.toprint('IMAGE_CONVERT_GRAY')

        image_out = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        self.message.toprint('IMAGE_CONVERTED_GRAY')

        return image_out
