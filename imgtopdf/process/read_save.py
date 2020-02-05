"""
    Read image
"""

# Third-party imports
import cv2

# Own imports
from utils.base import BaseClass


class ReadSave(BaseClass):

    def read(self, patch):
        """
            Read image. Image contents are compatible with OpenCV
        """

        image_out = cv2.imread(patch)

        return image_out

    def save(self, patch, image):
        """
            Save image
        """

        cv2.imwrite(
            patch.replace('.jpg', '.png'),
            image,
            [int(cv2.IMWRITE_PNG_COMPRESSION), 7]
        )
