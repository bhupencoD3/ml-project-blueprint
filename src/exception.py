import sys


def error_message_detail(error, error_detail: sys):
    """
    Returns a detailed error message including the script name,
    line number, and the error description.

    Args:
        error (Exception): The exception instance.
        error_detail (sys): The sys module, used to extract traceback details.

    Returns:
        str: A formatted error message with contextual information.
    """
    _, _, exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in script: [{0}] line number: [{1}] error message: [{2}]".format(
        filename, exc_tb.tb_lineno, str(error)
    )
    return error_message


class CustomException(Exception):
    """
    A custom exception class that enhances standard exceptions
    with detailed contextual information such as the script name
    and line number where the error occurred.
    """

    def __init__(self, error_message, error_detail: sys):
        """
        Initializes the CustomException instance.

        Args:
            error_message (str): The original error message.
            error_detail (sys): The sys module for traceback extraction.
        """
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self):
        """
        Returns the detailed error message when the exception is printed.

        Returns:
            str: Formatted error message.
        """
        return self.error_message
