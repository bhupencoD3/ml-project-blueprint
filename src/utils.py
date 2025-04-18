import os
import pickle
import sys

from src.exception import CustomException
from src.logger import logging


def save_object(file_path, obj):
    """
    Save any Python object (like a preprocessor, model, etc.) to disk using pickle.

    This function ensures that the directory exists before attempting to save,
    and handles errors gracefully by raising a custom exception.

    Args:
        file_path (str): Full path (including filename) where the object will be saved.
        obj (Any): The Python object you want to save (e.g., model, transformer).

    Raises:
        CustomException: If any issue occurs during saving.
    """
    try:
        # Extract directory path from the file path
        directory_path = os.path.dirname(file_path)

        # Create the directory if it doesn't already exist
        os.makedirs(directory_path, exist_ok=True)

        # Open the file in write-binary mode and dump the object using pickle
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)

        logging.info(f"📦 Object saved successfully at: {file_path}")

    except Exception as e:
        logging.error("❌ Failed to save object using pickle.")
        raise CustomException(e, sys) from e
