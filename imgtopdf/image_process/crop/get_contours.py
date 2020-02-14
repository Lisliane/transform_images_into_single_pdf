""" Get contours """

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>

# Third-party imports
import cv2

# Own imports
from utils.base import BaseClass


class GetContours(BaseClass):

    def apply(self, image):
        """
            Get contours of the image.
                where:
                    - image: array of image

                output:
                    - contours: array of contours
        """

        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if self.settings.CROP_THRESHOLD == 'ADAPTIVE':
            # Adaptive Thresholding: the algorithm determines the threshold for a pixel based on a
            #                        small region around it.
            #   where:
            #       - src: Source 8-bit single-channel image.
            #       - maxValue: Non-zero value assigned to the pixels for which the condition is
            #                   satisfied
            #       - adaptiveMethod: Adaptive thresholding algorithm to use.
            #                         * ADAPTIVE_THRESH_MEAN_C: The threshold value is the mean of
            #                                                   the neighbourhood area minus the
            #                                                   constant C.
            #                         * ADAPTIVE_THRESH_GAUSSIAN_C: The threshold value is a
            #                                                       gaussian-weighted sum of the
            #                                                       neighbourhood values minus the
            #                                                       constant C.
            #       - thresholdType: Thresholding type: THRESH_BINARY or THRESH_BINARY_INV.
            #       - blockSize: Size of a pixel neighborhood that is used to calculate a threshold
            #                    value for the pixel: 3, 5, 7, and so on.
            #       - C: Constant subtracted from the mean or weighted mean (see the details below).
            #            Normally, it is positive but may be zero or negative as well.
            image_thresh = cv2.adaptiveThreshold(
                src=image_gray,
                maxValue=self.settings.CROP_THRESHOLD_MAX,
                adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                thresholdType=cv2.THRESH_BINARY,
                blockSize=self.settings.CROP_THRESHOLD_BLOCK_SIZE,
                C=self.settings.CROP_THRESHOLD_C
            )

        elif self.settings.CROP_THRESHOLD == 'BINARY':
            # The function cv.threshold is used to apply the thresholding.
            #   where:
            #       - source: Input image array in grayscale
            #       - thresh: Value of Threshold below and above which pixel values will change
            #                 accordingly.
            #       - maxval: Maximum value that can be assigned to a pixel.
            #       - type: The type of thresholding to be applied.
            _, image_thresh = cv2.threshold(
                src=image_gray,
                thresh=self.settings.CROP_THRESHOLD_VALUE,
                maxval=self.settings.CROP_THRESHOLD_MAX,
                type=cv2.THRESH_BINARY
            )

        # Finds contours in a binary image.
        #   where:
        #       - image: Source 8-bit single-channel image.
        #       - mode: Contour retrieval mode.
        #               * RETR_EXTERNAL: retrieves only the extreme outer contours.
        #               * RETR_LIST: retrieves all of the contours without establishing any
        #                            hierarchical relationships.
        #               * RETR_TREE: retrieves all of the contours and reconstructs a full
        #                            hierarchy of nested contours.
        #       - method: Contour approximation method.
        #                 * CHAIN_APPROX_NONE: stores absolutely all the contour points.
        #                 * CHAIN_APPROX_SIMPLE: compresses horizontal, vertical, and diagonal
        #                                        segments and leaves only their end points.
        #                                        For example, an up-right rectangular contour is
        #                                        encoded with 4 points.
        contours, hierarchy = cv2.findContours(
            image=image_thresh,
            mode=cv2.RETR_TREE,
            method=cv2.CHAIN_APPROX_SIMPLE
        )

        return contours
