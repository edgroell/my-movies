# Dictionary containing formatting options for text styling in the terminal.
formatting = {
    "bold": "\033[1m",
    "underline": "\033[4m",
    # "white": "\033[37m",
    "red": "\033[31m",
    "green": "\033[32m",
    "blue": "\033[34m",
    "reset": "\033[0m"
}


class TextFormatter:
    @staticmethod
    def title(message):
        """ Format the message as a title with underline and bold styling. """
        return f"{formatting['underline']}{formatting['bold']}{message}{formatting['reset']}"

    @staticmethod
    def prompt(message):
        """ Format the message as a prompt (i.e., interaction with the user) with blue and bold styling. """
        return f"{formatting['blue']}{formatting['bold']}{message}{formatting['reset']}"

    @staticmethod
    def success(message):
        """ Format the message as a success with green and bold styling. """
        return f"{formatting['green']}{formatting['bold']}{message}{formatting['reset']}"

    @staticmethod
    def error(message):
        """ Format the message as an error with red and bold styling. """
        return f"{formatting['red']}{formatting['bold']}{message}{formatting['reset']}"
