""" Auto crop """

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>

# Own imports
from .cut_border import CutBorder
from .get_contours import GetContours
from .max_contour import MaxContour
from utils.base import BaseClass


class Crop(BaseClass):

    def __init__(self, language=None):
        """
            - language: language of messages
        """

        super().__init__(language)

        self.get_contours = GetContours(language)

    def apply(self, image):
        """
            Crop image principal.
                where:
                    - image: array of image

                output:
                    - image_out: array of image cropped
        """

        self.message.toprint('IMAGE_CROP')

        bounds = self.get_contours.apply(image)
        max_contour = MaxContour.apply(bounds)
        image_out = CutBorder.apply(image, max_contour)

        self.message.toprint('IMAGE_CROPED')

        return image_out
