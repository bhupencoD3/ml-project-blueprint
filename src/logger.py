import logging
import os
from datetime import datetime

# Generate the log file name based on the current date
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d')}.log"

# Define the path to store the log file
# Combines the current working directory with the "logs" folder and the log file name
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# Create the "logs" folder if it doesn't exist.
# The exist_ok=True parameter means it won't raise an error if the folder already exists.
os.makedirs(logs_path, exist_ok=True)

# Full path to the log file, combining the folder and the file name
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Set up logging configuration
# This will create a log file and write logs in a specific format: [timestamp] log level [file:line] log message
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Where to store the logs
    format="[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d] %(message)s",  # Log format includes timestamp, log level, filename, line number, and message
    level=logging.INFO,  # Log messages at the INFO level or higher
)


"""
This script defines a basic logging system for storing log messages in a dynamically generated log file.

- It creates a log file with the current date as the name (e.g., "2025-04-13.log").
- It checks if the "logs" directory exists and creates it if necessary.
- It configures the logging system to log messages with a timestamp, log level, file name, line number, and the log message itself.
- The logging level is set to INFO, so only messages at INFO level and above (WARNING, ERROR, CRITICAL) are recorded.
"""
