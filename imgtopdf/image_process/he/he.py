""" Histogram equalization """

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>

# Third-party imports
import cv2

# Own imports
from utils.base import BaseClass


class HistogramEqualization(BaseClass):

    def apply(self, image):
        """
            Applying histogram equalization.
                where:
                    - image: array of image

                output:
                    - image: array of image with histogram equalization
        """

        self.message.toprint('IMAGE_APPLY_HE')

        # Base class for Contrast Limited Adaptive Histogram Equalization.
        #   Parameters:
        #       - clipLimit: Threshold for contrast limiting.
        #       - tileGridSize: Size of grid for histogram equalization.
        #                       Input image will be divided into equally sized rectangular tiles.
        #                       tileGridSize defines the number of tiles in row and column.
        clahe = cv2.createCLAHE(
            clipLimit=self.settings.HE_CLIP_LIMIT,
            tileGridSize=(self.settings.HE_TILE_GRID_SIZE, self.settings.HE_TILE_GRID_SIZE)
        )
        image[:, :, 0] = clahe.apply(image[:, :, 0])
        image[:, :, 1] = clahe.apply(image[:, :, 1])
        image[:, :, 2] = clahe.apply(image[:, :, 2])

        self.message.toprint('IMAGE_APPLIED_HE')

        return image
