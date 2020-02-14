#!/usr/bin/env python

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>

# Third-party imports
import argparse

# Own imports
from image_process import Process as ProcessImage
from pdf_generate import Process as ProcessPDF


def parse_args():
    parser = argparse.ArgumentParser()

    help_msg = 'Options: 1-Treats images   2-Generates PDF only'
    parser.add_argument(
        '--option',
        action='store',
        type=int,
        default=1,
        choices=[1, 2],
        help=help_msg
    )

    help_msg = 'Defines language. Options: PTB (portuguese)  ENG (english)'
    parser.add_argument(
        '--lang',
        action='store',
        type=str,
        default='PTB',
        help=help_msg
    )

    args = parser.parse_args()
    return args


def main():
    """
        Main
    """

    args = parse_args()
    lang = args.lang
    option = args.option

    process_image = ProcessImage(language=lang)
    process_pdf = ProcessPDF(language=lang)

    if option == 1:
        process_image.apply()

    process_pdf.apply()


if __name__ == '__main__':
    main()
