"""
    Principal process
"""

# Third-party imports
from utils import constant
from process.copy_dir import CopyDir

# Own imports
from utils.base import BaseClass


class Process(BaseClass):

    def run(self):

        copydir = CopyDir(language=self.language)
        copydir.run(constant.PATCH_SOURCE, constant.PATCH_DESTINY)
