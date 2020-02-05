"""
    Retinex algorithm
"""

# Third-party imports
import numpy as np
import cv2

# Own imports
from utils import constant
from utils.base import BaseClass


class Retinex(BaseClass):
    """
        The use of Retinex might be beneficial to images processing:
            * that are hazy, misty or having a veil of fog
            * with important luminance gaps
    """

    @staticmethod
    def retinex_scales_distribution(max_scale, nr_scale):
        """
           Specifies iterations of the multiscale filter

           Parameters:
                - max_scale: maximum value of scale
                - nr_scale: number of retinex effect interactions
        """

        scales = []
        scale_step = max_scale / nr_scale
        for _scale in range(nr_scale):
            scales.append(scale_step * _scale + 2.0)

        return scales

    @staticmethod
    def color_restoration(image_original, image_retinex, alpha, gain, offset):
        """
            Color Restoration function

            Parameters:
                - alpha : Controls the strength of nonlinearity. It's constant.
                - gain  : will act on the total amplitude by increasing or decreasing it and
                          for example reduce the numbe of totally black pixels.
                          It's constant.
                - offset: Brightness = will allow to reset the luminance after "Gain" acted.
                          It's constant.
        """

        image_color_restoration = image_retinex * gain * (
            np.log(
                alpha * (image_original + 1.0)
            ) - np.log(np.sum(image_original, axis=2) + 3.0)[:, :, np.newaxis]
        ) + offset

        return image_color_restoration

    def MSRCR(self, image):
        """
            MSRCR (Multi-Scale Retinex with Color Restoration) is a retinex based algorithm
            that uses logarithmic compression and spatial convolution.
            MSRCR combines the dynamic range compression and color constancy of the MSR with
            a color 'restoration' filter that provides excellent color rendition.
        """

        self.message.toprint('IMAGE_APPLY_MSRCR')

        # Color channels in order R G B
        image_original = np.float32(cv2.cvtColor(image, cv2.COLOR_GRAY2RGB))

        # Distributes scale interactions
        max_scale = constant.RETINEX_MAX_SCALE
        nr_scale = constant.RETINEX_NR_SCALE
        scales = self.retinex_scales_distribution(max_scale, nr_scale)

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

        alpha = constant.RETINEX_ALPHA
        gain = constant.RETINEX_GAIN
        offset = constant.RETINEX_OFFSET

        image_retinex = self.color_restoration(
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
        k = constant.RETINEX_DYNAMIC

        image_mini = image_mean - k * image_std

        image_maxi = image_mean + k * image_std

        image_maxi_mini = image_maxi - image_mini

        image_oldT_mini = image_retinex - image_mini
        image_out = np.uint8(np.clip(image_oldT_mini / image_maxi_mini * 255, 0, 255))

        self.message.toprint('IMAGE_APPLIED_MSRCR')

        return image_out
