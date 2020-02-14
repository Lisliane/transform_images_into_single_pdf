""" Specifies iterations of the multiscale filter """

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>


class ScalesDistribution:

    @staticmethod
    def apply(max_scale, nr_scale):
        """
            Specifies iterations of the multiscale filter.
                where:
                    - max_scale: maximum value of scale
                    - nr_scale: number of retinex effect interactions

                output:
                    - scales: number of distributed scale
        """

        scales = []
        scale_step = max_scale / nr_scale
        for _scale in range(nr_scale):
            scales.append(scale_step * _scale + 2.0)

        return scales
