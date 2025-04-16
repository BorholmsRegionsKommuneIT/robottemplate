import logging
import time
import pandas as pd
from opuspy import say_hello_from_opuspy
from brkrpautils import Config

# Used by ExampleChildConfig
import os
import json
from pathlib import Path
from topdeskpy import Topdeskclient

# init config and logger
config = Config()
log = logging.getLogger(__name__)

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)

# Make directory for the report at DATA_FOLDER_SESSION_PATH, if it does not exist
config.DATA_FOLDER_SESSION_PATH.mkdir(parents=True, exist_ok=True)


input_dfs = {}

for file_path in config.DATA_FOLDER_PATH.glob("input*.csv"):
    key = file_path.stem
    # Reading the CSV file and storing it in the dictionary. All cols as strings
    input_dfs[key] = pd.read_csv(filepath_or_buffer=file_path, sep=";", dtype=str)


def main():
    say_hello_from_opuspy()
    extendedConfig = ExampleChildConfig()
    extendedConfig.hello_from_child_class()


class ExampleChildConfig(Config):
    def __init__(self):
        super().__init__()

        self.YOUR_VERY_OWN_VARIABLE_HERE = "Hi mom! I'm a robot now!"
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

    def hello_from_child_class(self):
        log.info(self.YOUR_VERY_OWN_VARIABLE_HERE)


if __name__ == "__main__":
    try:
        start_time = time.time()
        main()
        end_time = time.time()
        log.info(f"the process took {round(end_time - start_time)} seconds")

    except:
        # report to Topdek only if running on server
        if config.COMPUTERNAME.startswith(config.SERVER_PREFIX):
            config.TOPDESK_CLIENT.create_incident(
                request=f"{config.ROBOTUSER} - {config.ROBOT_DESCRIPTION} - failed",
                callType="Information",
            )
        raise
