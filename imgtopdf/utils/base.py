""" Base class """

# Authors: Lisliane Zanette de Oliveira <lislianezanetteoliveira@gmail.com>


# Third-party imports
from abc import ABC

# Own imports
from utils import settings
from utils.print_message import Message


class BaseClass(ABC):
    """
        Base class
    """

    def __init__(self, language=None):
        """
            - language: language of messages
        """

        self.language = language
        self.message = Message(language)
        self.settings = settings
