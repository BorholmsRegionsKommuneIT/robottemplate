import os
from pathlib import Path
import datetime
from dotenv import load_dotenv  # python-dotenv
import logging


class Config:
    def __init__(self, download_mode, sample_mode):
        load_dotenv(override=True)
        self.COMPUTERNAME = os.environ["COMPUTERNAME"]
        self.TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.AUTOMATIKDATA_PATH = Path(os.getenv("AUTOMATIKDATA_PATH"))
        self.BRK_PAM_PATH = Path(os.getenv("BRK_PAM_PATH"))
        self.ROBOTUSER = os.getenv("ROBOTUSER")
        self.PROCESS_ID = int(os.getenv("PROCESS_ID"))
        self.ROBOT_DESCRIPTION = os.getenv("ROBOT_DESCRIPTION")
        self.SERVER_PREFIX = os.getenv("SERVER_PREFIX")
        self.TOPDESK_BASE_URL = os.getenv("TOPDESK_BASE_URL")

        # Modes explicitly set during initialization
        self.DOWNLOAD_MODE = download_mode
        self.SAMPLE_MODE = sample_mode

        # Derived paths
        self.DATA_FOLDER_PATH = Path(f"{self.AUTOMATIKDATA_PATH}/{self.ROBOTUSER}/data")
        self.LOGS_FOLDER_PATH = Path(f"{self.AUTOMATIKDATA_PATH}/{self.ROBOTUSER}/logs")
        self.PAM_PATH_SHARED = Path(f"{self.BRK_PAM_PATH}/SharedFiles")
        self.PAM_PATH_ROBOT = Path(f"{self.BRK_PAM_PATH}/{self.ROBOTUSER}/{self.ROBOTUSER}.json")
        self.DATA_FOLDER_SESSION_PATH = Path(f"{self.DATA_FOLDER_PATH}/{self.TIMESTAMP}")

        if self.COMPUTERNAME.startswith(self.SERVER_PREFIX):
            self.DOWNLOAD_MODE = 1

        # Configure the logger
        self.LOG_FILE = Path(f"{self.AUTOMATIKDATA_PATH}/{self.ROBOTUSER}/logs", f"{self.TIMESTAMP}.log")

        # Define the logger configuration
        logger = logging.getLogger()

        # Set the lowest-level logger (root logger) to DEBUG so it will catch all logs
        logger.setLevel(logging.DEBUG)

        # Create a handler for writing logs to the console
        console_handler = logging.StreamHandler()

        # Create a handler for writing logs to the log file
        file_handler = logging.FileHandler(self.LOG_FILE)

        # Create a custom formatter to include module name and line number in the log output
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(module)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Attach the formatter to the handlers
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add the handler to the logger if it hasn't been added yet
        if not logger.handlers:
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)

        self.logger = logging.getLogger(__name__)

    def __repr__(self):
        return (
            f"COMPUTERNAME={self.COMPUTERNAME},\n"
            f"TIMESTAMP={self.TIMESTAMP},\n"
            f"AUTOMATIKDATA_PATH={self.AUTOMATIKDATA_PATH},\n"
            f"BRK_PAM_PATH={self.BRK_PAM_PATH},\n"
            f"ROBOTUSER={self.ROBOTUSER},\n"
            f"PROCESS_ID={self.PROCESS_ID},\n"
            f"ROBOT_DESCRIPTION={self.ROBOT_DESCRIPTION},\n"
            f"SERVER_PREFIX={self.SERVER_PREFIX},\n"
            f"TOPDESK_BASE_URL={self.TOPDESK_BASE_URL},\n"
            f"DOWNLOAD_MODE={self.DOWNLOAD_MODE},\n"
            f"SAMPLE_MODE={self.SAMPLE_MODE},\n"
            f"LOG_FILE={self.LOG_FILE},\n"
            f"DATA_FOLDER_PATH={self.DATA_FOLDER_PATH},\n"
            f"LOGS_FOLDER_PATH={self.LOGS_FOLDER_PATH},\n"
            f"PAM_PATH_SHARED={self.PAM_PATH_SHARED},\n"
            f"PAM_PATH_ROBOT={self.PAM_PATH_ROBOT},\n"
            f"DATA_FOLDER_SESSION_PATH={self.DATA_FOLDER_SESSION_PATH}\n"
        )
