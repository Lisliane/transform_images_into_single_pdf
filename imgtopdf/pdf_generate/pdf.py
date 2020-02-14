""" Converts image to pdf """

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>

# Third-party imports
from fpdf import FPDF
from PIL import Image

# Own imports
from utils.base import BaseClass


class ConvertToPDF(BaseClass):

    def __init__(self, language=None):
        """
            - language: language of messages
        """

        super().__init__(language)

        self.pdf = FPDF(unit='mm', format='A4')
        self.pdf.set_compression(True)

        # A4 format size
        self.pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

    def apply(self, patch, page):
        """
            Converts image to file pdf.
                where:
                    - path: directory where the images are
                    - page: integer number page
        """

        self.message.toprint('IMAGE_CREATE_PDF')

        cover = Image.open(patch)
        width, height = cover.size

        # convert pixel in mm with 1px=0.264583 mm
        width, height = float(width * 0.264583), float(height * 0.264583)

        # get page orientation from image size
        orientation = 'P' if width < height else 'L'

        #  make sure image size is not greater than the pdf format size
        width = width if width < self.pdf_size[orientation]['w'] else self.pdf_size[orientation]['w']
        height = height if height < self.pdf_size[orientation]['h'] else self.pdf_size[orientation]['h']

        # center image
        self.pdf.add_page(orientation=orientation)
        self.pdf.image(patch, self.settings.PDF_X, self.settings.PDF_Y, width, height)

        self.message.toprint('IMAGE_CREATED_PDF', {'page': page})

    def save(self, file_destin):
        """
            Save image to file pdf.
                where:
                    - file_destin: name file destiny
        """

        self.message.toprint('SAVE_PDF')

        self.pdf.output(file_destin, 'F')

        self.message.toprint('SAVED_PDF')
