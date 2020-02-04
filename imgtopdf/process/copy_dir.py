"""
    Copies the original images to a working directory
"""

# Third-party imports
import cv2
import glob
import os

# Own imports
from utils.base import BaseClass


class CopyDir(BaseClass):

    def run(self, path_source, patch_destiny):

        self.message.toprint('COPY_IMAGE')

        # If directory does not exist, create
        if not os.path.exists(patch_destiny):
            self.message.toprint('CREATE_PATH', {'patch': patch_destiny})
            os.makedirs(patch_destiny)

        # If directory does exist, delete files from path
        else:
            self.message.toprint('DELETE_FILES_FROM_PATH', {'patch': patch_destiny})
            files = glob.glob('{0}/*'.format(patch_destiny))
            for f in files:
                os.remove(f)

        for root, subdirectories, files in os.walk(path_source):
            for file in files:
                image = cv2.imread(os.path.join(root, file))
                cv2.imwrite(os.path.join(patch_destiny, file), image)

        self.message.toprint('IMAGE_COPIED')
