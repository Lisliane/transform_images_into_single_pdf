""" Rotate image """

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>

# Third-party imports
import cv2
import math
import numpy as np
from scipy import ndimage

# Own imports
from utils.base import BaseClass


class Rotate(BaseClass):

    def apply(self, image):
        """
            Rotate image.
                where:
                    - image: array of image

                output:
                    - image_out: array of image rotated
        """

        self.message.toprint('ROTATE_IMAGE')
        image_out = image

        # Median of the single channel pixel intensities
        median_image = np.median(image)

        # Automatic canny edge detection using the computed median
        auto_threshold1 = int(max(0, (1.0 - self.settings.ROTATE_SIGMA) * median_image))
        auto_threshold2 = int(min(255, (1.0 + self.settings.ROTATE_SIGMA) * median_image))

        # Edge detector with canny
        #   where:
        #       - image: single-channel 8-bit input image
        #       - threshold1: first threshold for the hysteresis procedure
        #       - threshold2: second threshold for the hysteresis procedure
        #       - apertureSize: aperture size for the Sobel() operator
        img_edge = cv2.Canny(
            image=image,
            threshold1=auto_threshold1,
            threshold2=auto_threshold2,
            apertureSize=self.settings.ROTATE_APERTURE_SIZE
        )

        # Progressive Probabilistic Hough Transform (cv2.HoughLinesP)
        #   where:
        #       - image: output of the edge detector
        #       - rho: distance resolution of the accumulator in pixels
        #       - theta: angle resolution of the accumulator in radians
        #       - threshold: minimum number of intersections to detect a line
        #       - minLinLength: minimum length of line.
        #                       Line segments shorter than this are rejected.
        #       - maxLineGap: maximum allowed gap between line segments to treat them as
        #                     single line.
        lines = cv2.HoughLinesP(
            image=img_edge,
            rho=self.settings.ROTATE_HLP_RHO,
            theta=math.pi / 180,
            threshold=self.settings.ROTATE_HLP_THRESHOLD,
            minLineLength=self.settings.ROTATE_HLP_MIN_LINE_LENGTH,
            maxLineGap=self.settings.ROTATE_HLP_MAX_LINE_GAP
        )

        # Identify lines
        if lines is not None:
            angles = []
            for i in range(0, len(lines)):
                line_points = lines[i][0]
                line_x1 = line_points[0]
                line_y1 = line_points[1]
                line_x2 = line_points[2]
                line_y2 = line_points[3]

                # calculate angle radian
                angle = math.degrees(math.atan2(line_y2 - line_y1, line_x2 - line_x1))
                angles.append(angle)

            # Median of the given data along the specified axis (np.median)
            median_angle = np.median(angles)

            if median_angle != 0:
                # Rotate an image from North to East given an angle in degrees (ndimage.rotate)
                #   where:
                #       - input: data array of original image
                #       - angle: angle in degrees
                image_out = ndimage.rotate(
                    input=image,
                    angle=median_angle
                )

        self.message.toprint('IMAGE_ROTATED')

        return image_out
