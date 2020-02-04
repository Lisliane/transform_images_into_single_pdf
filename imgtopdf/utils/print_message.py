"""
    Print messages
"""

# Own imports
from utils import message_dict


class Message():

    def __init__(self, language=None):
        """
            Parameters:
                - language:
        """

        self.language = language

    def toprint(self, message=None, values_dict={}):
        """
            Parameters:
                - message:
                - values_dict:
        """

        if message is not None:
            msg = getattr(message_dict, message) or None
            if msg is not None:
                result_msg = msg.get(self.language) or None
                if result_msg is not None:
                    if values_dict == {}:
                        print(result_msg)
                    else:
                        print(result_msg.format(**values_dict))
