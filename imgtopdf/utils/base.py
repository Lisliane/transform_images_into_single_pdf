"""
    Base class
"""

# Third-party imports
from abc import ABC

# Own imports
from utils.print_message import Message


class BaseClass(ABC):
    """
        Base class
    """

    def __init__(self, language=None):
        """
            Parameters:
                - language:
        """

        self.language = language
        self.message = Message(language)
