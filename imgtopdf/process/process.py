"""
    Principal process
"""

# Third-party imports
import os

# Own imports
from utils import constant
from utils.base import BaseClass
from process.copy_dir import CopyDir
from process.crop import Crop
from process.gray import ConvertToGray
from process.he import HistogramEqualization
from process.read_save import ReadSave
from process.retinex import Retinex
from process.rotate import Rotate


class Process(BaseClass):

    def run_image(self):
        read_save = ReadSave(language=self.language)
        gray = ConvertToGray(language=self.language)
        crop = Crop(language=self.language)
        rotate = Rotate(language=self.language)
        he = HistogramEqualization(language=self.language)
        retinex = Retinex(language=self.language)

        # Copies the original images to a working directory
        copydir = CopyDir(language=self.language)
        copydir.run(constant.PATCH_SOURCE, constant.PATCH_DESTINY)

        for root, subdirectories, files in os.walk(constant.PATCH_DESTINY):
            for file in files:
                self.message.toprint('IMAGE_PROCESS', {'file': file})
                patch = os.path.join(root, file)
                image = read_save.read(patch)
                image = gray.apply(image)
                image = crop.apply(image)
                image = he.apply(image)
                image = retinex.MSRCR(image)
                image = rotate.apply(image)
                read_save.save(patch, image)

                self.message.toprint('IMAGE_PROCESSED', {'file': file})

    def run(self, option=1):
        if option == 1:
            self.run_image()
