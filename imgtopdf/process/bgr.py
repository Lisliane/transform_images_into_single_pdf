"""
    Converts image to BGR scale
"""

# Third-party imports
import cv2

# Own imports
from utils.base import BaseClass


class ConvertToBGR(BaseClass):

    def apply(self, image):
        """
            Converts image to BGR
        """

        self.message.toprint('IMAGE_CONVERT_BGR')

        image_out = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        self.message.toprint('IMAGE_CONVERTED_BGR')

        return image_out
