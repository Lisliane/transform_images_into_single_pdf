""" Read and save image """

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>

# Third-party imports
import cv2

# Own imports
from utils.base import BaseClass


class ReadSave(BaseClass):

    def read(self, patch):
        """
            Read image. Image contents are compatible with OpenCV.
                where:
                    - path: directory where the images are

                output:
                    - image_out: array of image
        """

        image_out = cv2.imread(patch)

        return image_out

    def save(self, patch, image):
        """
            Save image.
                where:
                    - path: directory where the images are
                    - image: array of image
        """

        cv2.imwrite(
            patch.replace(self.settings.EXTENSION_TO_EDIT, self.settings.EXTENSION_TO_OUTPUT),
            image,
            [int(cv2.IMWRITE_PNG_COMPRESSION), 7]
        )
