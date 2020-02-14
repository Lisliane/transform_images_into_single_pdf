""" Principal process - image"""

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>

# Third-party imports
import os

# Own imports
from utils.base import BaseClass
from .crop import Crop
from .he import HistogramEqualization
from .retinex import Retinex
from .rotate import Rotate
from .file_manage import CopyDir, ReadSave


class Process(BaseClass):

    def __init__(self, language=None):
        """
            - language: language of messages
        """

        super().__init__(language)

        self.copydir = CopyDir(language=language)
        self.read_save = ReadSave(language=language)
        self.crop = Crop(language=language)
        self.rotate = Rotate(language=language)
        self.he = HistogramEqualization(language=language)
        self.retinex = Retinex(language=language)

    def apply(self):
        # Copies the original images to a working directory
        self.copydir.run(self.settings.PATCH_SOURCE, self.settings.PATCH_DESTINY)

        for root, subdirectories, files in os.walk(self.settings.PATCH_DESTINY):
            files.sort()
            for file in files:
                if file.endswith(self.settings.EXTENSION_TO_EDIT):
                    self.message.toprint('IMAGE_PROCESS', {'file': file})
                    patch = os.path.join(root, file)
                    image = self.read_save.read(patch)

                    # Apply retinex algorithm
                    if self.settings.RUN_RETINEX:
                        image = self.retinex.MSRCR(image)

                    # Apply histogram equalization
                    if self.settings.RUN_HISTOGRAM_EQUALIZATION:
                        image = self.he.apply(image)

                    # Apply histogram equalization
                    if self.settings.RUN_CROP:
                        image = self.crop.apply(image)

                    # Apply image rotation
                    if self.settings.RUN_ROTATE:
                        image = self.rotate.apply(image)

                    self.read_save.save(patch, image)

                    self.message.toprint('IMAGE_PROCESSED', {'file': file})
