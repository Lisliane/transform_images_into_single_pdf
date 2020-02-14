""" Color Restoration """

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>

# Third-party imports
import numpy as np


class ColorRestoration:

    @staticmethod
    def apply(image_original, image_retinex, alpha, gain, offset):
        """
            Color Restoration function.
                where:
                    - alpha : Controls the strength of nonlinearity. It's constant.
                    - gain  : will act on the total amplitude by increasing or decreasing it and
                              for example reduce the numbe of totally black pixels.
                              It's constant.
                    - offset: Brightness = will allow to reset the luminance after "Gain" acted.
                              It's constant.

                output:
                    - image_color_restoration: array of image with color restoration
        """

        image_color_restoration = image_retinex * gain * (
            np.log(
                alpha * (image_original + 1.0)
            ) - np.log(np.sum(image_original, axis=2) + 3.0)[:, :, np.newaxis]
        ) + offset

        return image_color_restoration
