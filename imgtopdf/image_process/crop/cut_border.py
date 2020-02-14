""" Cut border from image """

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>


class CutBorder:

    @staticmethod
    def apply(image, boundaries):
        """
            Crop image.
                where:
                    - image: array of image
                    - boundaries: outer edge

                output:
                    - image: array of image, taking the edge off
        """

        x_min, y_min, x_max, y_max = boundaries

        return image[y_min:y_max, x_min:x_max]
