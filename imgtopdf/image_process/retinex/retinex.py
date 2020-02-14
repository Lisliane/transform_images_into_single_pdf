""" Retinex algorithm """

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>

# Third-party imports
import cv2
import numpy as np

# Own imports
from .color_restoration import ColorRestoration
from .scales_distribution import ScalesDistribution
from utils.base import BaseClass


class Retinex(BaseClass):
    """
        The use of Retinex might be beneficial to images processing:
            * that are hazy, misty or having a veil of fog
            * with important luminance gaps
    """

    def MSRCR(self, image):
        """
            MSRCR (Multi-Scale Retinex with Color Restoration) is a retinex based algorithm
            that uses logarithmic compression and spatial convolution.
            MSRCR combines the dynamic range compression and color constancy of the MSR with
            a color 'restoration' filter that provides excellent color rendition.
                where:
                    - image: array of image

                output:
                    - image_out: array of image treated
        """

        self.message.toprint('IMAGE_APPLY_MSRCR')

        image_original = np.float32(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Distributes scale interactions
        max_scale = self.settings.RETINEX_MAX_SCALE
        nr_scale = self.settings.RETINEX_NR_SCALE
        scales = ScalesDistribution.apply(max_scale, nr_scale)

        # new image with zero channels
        image_blur = np.zeros(
            shape=[
                len(scales),
                image_original.shape[0],
                image_original.shape[1],
                image_original.shape[2]
            ]
        )

        # new image with zero channels
        image_mlog = np.zeros(
            shape=[
                len(scales),
                image_original.shape[0],
                image_original.shape[1],
                image_original.shape[2]
            ]
        )

        # Do for each channel
        for channel in range(3):
            # Do for each scale distributed
            for scale_count, scale in enumerate(scales):

                # If sigma==0, it will be automatically calculated based on scale
                image_blur[scale_count, :, :, channel] = cv2.GaussianBlur(
                    image_original[:, :, channel], (0, 0), scale
                )
                image_mlog[scale_count, :, :, channel] = np.log(
                    image_original[:, :, channel] + 1.
                ) - np.log(
                    image_blur[scale_count, :, :, channel] + 1.
                )

        image_retinex = np.mean(image_mlog, 0)

        alpha = self.settings.RETINEX_ALPHA
        gain = self.settings.RETINEX_GAIN
        offset = self.settings.RETINEX_OFFSET

        image_retinex = ColorRestoration.apply(
            image_original=image_original,
            image_retinex=image_retinex,
            alpha=alpha,
            gain=gain,
            offset=offset
        )

        # Average color image retinex whith restoration
        image_mean = np.mean(image_retinex)

        # Standard deviation image retinex whith color restoration
        image_std = np.std(image_retinex)

        # Tansmission Map
        #   The processing consist of to apply, using the "Transmission Map" average and
        #   standard-deviation, a transformation of the type:
        #       * newT = (oldT-mini) / (maxi-mini)
        #           * with mini = average - k * standard-deviation
        #           * with maxi = average + k * standard-deviation
        # where k = retinex_dynamic = contrast (variance): is decisive in the image rendering:
        #   * low values will increase the seeming contrast,
        #   * hight values will make the image more natural with less artefacts and hazes.
        k = self.settings.RETINEX_DYNAMIC

        image_mini = image_mean - k * image_std

        image_maxi = image_mean + k * image_std

        image_maxi_mini = image_maxi - image_mini

        image_oldT_mini = image_retinex - image_mini
        image_out = np.uint8(np.clip(image_oldT_mini / image_maxi_mini * 255, 0, 255))

        image_out = cv2.cvtColor(image_out, cv2.COLOR_RGB2BGR)

        self.message.toprint('IMAGE_APPLIED_MSRCR')

        return image_out
