import cv2
import os


class CopyDir:

    def run(self, path_source, patch_destiny):

        print('Copy images...')
        # If directory does not exist, create
        if not os.path.exists(patch_destiny):
            print('Create patch: {0}'.format(patch_destiny))
            os.makedirs(patch_destiny)

        for root, subdirectories, files in os.walk(path_source):
            for file in files:
                image = cv2.imread(os.path.join(root, file))
                cv2.imwrite(os.path.join(patch_destiny, file), image)

        print('Image copied.')
