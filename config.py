import os
from pathlib import Path
import logging
import json
from datetime import datetime, timedelta
from topdeskpy import Topdeskclient
from dotenv import load_dotenv  # pip install python-dotenv


class Config:
    def __init__(self):
        # Manually set DOWNLOAD_MODE, SAMPLE_MODE, CUSTOM_YEAR_MONTH
        self.DOWNLOAD_MODE = 0  # 1 will download from opus, 0 will not. Possible to download new an old year_months.
        self.SAMPLE_MODE = 0  # l will use sample cpr from input_cpr_test.csv
        self.YEAR_MONTH = "2024-06"  # Will be overwritten if run on server
        load_dotenv(override=True)
        # Read path to remote .env from local .env
        self.DOTENV_PATH = Path(os.getenv("DOTENV_PATH"))

        if self.DOTENV_PATH.exists():
            load_dotenv(dotenv_path=self.DOTENV_PATH, override=True)

        # Read environment variables from remote .env
        self.TIMESTAMP = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.COMPUTERNAME = os.environ["COMPUTERNAME"]
        self.AUTOMATIKDATA_PATH = Path(os.getenv("AUTOMATIKDATA_PATH"))
        self.BRK_PAM_PATH = Path(os.getenv("BRK_PAM_PATH"))
        self.ROBOTUSER = os.getenv("ROBOTUSER")
        self.PROCESS_ID = int(os.getenv("PROCESS_ID"))
        self.ROBOT_DESCRIPTION = os.getenv("ROBOT_DESCRIPTION")
        self.SERVER_PREFIX = os.getenv("SERVER_PREFIX")

        # On Server always download and run the previous month
        if self.COMPUTERNAME.startswith(self.SERVER_PREFIX):
            self.DOWNLOAD_MODE = 1
            self.SAMPLE_MODE = 0
            date_obj = datetime.strptime(self.TIMESTAMP, "%Y-%m-%d-%H-%M-%S").date()
            previous_month = date_obj.replace(day=1) - timedelta(days=1)
            self.YEAR_MONTH = f"{previous_month.year}-{previous_month.month:02d}"

        # ------------------------------- Derived paths ------------------------------ #
        self.DATA_FOLDER_PATH = Path(f"{self.AUTOMATIKDATA_PATH}/{self.ROBOTUSER}/data")
        self.LOGS_FOLDER_PATH = Path(f"{self.AUTOMATIKDATA_PATH}/{self.ROBOTUSER}/logs")
        self.INPUT_FOLDER_PATH = Path(f"{self.AUTOMATIKDATA_PATH}/{self.ROBOTUSER}/input")
        self.PAM_PATH_SHARED = Path(f"{self.BRK_PAM_PATH}/SharedFiles")
        self.PAM_PATH_ROBOT = Path(f"{self.BRK_PAM_PATH}/{self.ROBOTUSER}/{self.ROBOTUSER}.json")
        self.DATA_FOLDER_SESSION_PATH = Path(f"{self.DATA_FOLDER_PATH}/{self.YEAR_MONTH}")

        # ---------------------------------------------------------------------------- #
        #                                     Opus                                     #
        # ---------------------------------------------------------------------------- #
        self.SAPSHCUT_PATH = Path(os.getenv("SAPSHCUT_PATH"))

        # ---------------------------------------------------------------------------- #
        #                             Rollebaseret Indgang                             #
        # ---------------------------------------------------------------------------- #
        self.RI_URL = Path(os.getenv("RI_URL"))

        # ---------------------------------------------------------------------------- #
        #                                    Topdesk                                   #
        # ---------------------------------------------------------------------------- #
        self.TOPDESK_BASE_URL = os.getenv("TOPDESK_BASE_URL")
        with open(Path(f"{self.PAM_PATH_SHARED}/topdesk.json"), "r") as file:
            topdesk_credentials = json.load(file)
        self.TD_USERNAME = topdesk_credentials.get("username")
        self.TD_PASSWORD = topdesk_credentials.get("password")

        self.TOPDESK_CLIENT = Topdeskclient(self.TOPDESK_BASE_URL, self.TD_USERNAME, self.TD_PASSWORD)

        # ---------------------------------------------------------------------------- #
        #                                    Logger                                    #
        # ---------------------------------------------------------------------------- #

        # Configure the logger
        self.LOG_FILE = Path(
            f"{self.AUTOMATIKDATA_PATH}/{self.ROBOTUSER}/logs",
            f"{self.TIMESTAMP}.log",
        )

        # Define the logger configuration
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

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

        self.logger = logging.getLogger(__name__)  # Clould also be self.logger = logger
