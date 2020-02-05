"""
    Histogram equalization
"""

# Third-party imports
import cv2

# Own imports
from utils.base import BaseClass


class HistogramEqualization(BaseClass):

    def apply(self, image):
        """
            Applying histogram equalization
        """

        self.message.toprint('IMAGE_APPLY_HE')

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        image_result = clahe.apply(image)

        self.message.toprint('IMAGE_APPLIED_HE')

        return image_result
