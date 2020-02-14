""" Principal process - pdf """

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>

# Third-party imports
import os

# Own imports
from utils.base import BaseClass
from .pdf import ConvertToPDF


class Process(BaseClass):

    def __init__(self, language=None):
        """
            - language: language of messages
        """

        super().__init__(language)

        self.pdf = ConvertToPDF(language=language)

    def apply(self):

        page = 0

        for root, subdirectories, files in os.walk(self.settings.PATCH_DESTINY):
            files.sort()
            for file in files:
                if file.endswith(self.settings.EXTENSION_TO_OUTPUT):

                    self.message.toprint('IMAGE_PROCESS', {'file': file})
                    patch = os.path.join(root, file)
                    page += 1
                    self.pdf.apply(patch, page)

                    self.message.toprint('IMAGE_PROCESSED', {'file': file})

            self.pdf.save(self.settings.DESTINY_PDF)

        self.message.toprint('DONE')
