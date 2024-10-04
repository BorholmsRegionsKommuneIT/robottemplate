# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "python-dotenv",
#     "loguru",
#     "brkrpautils",
#     "os2apwrapper",
#     "topdeskpy",
# ]
# [tool.uv.sources]
# os2apwrapper = { git = "https://github.com/BorholmsRegionsKommuneIT/os2apwrapper" }
# topdeskpy = { git = "https://github.com/BorholmsRegionsKommuneIT/topdeskpy" }
# ///

import os
import time
import json
from pathlib import Path
import datetime

from dotenv import load_dotenv  # python-dotenv
from loguru import logger

# from os2apwrapper import ApiClient
from topdeskpy import Topdeskclient

# If using pandas
# pd.set_option("display.max_colwidth", None)

DOWNLOAD_MODE = 0
SAMPLE_MODE = 0
COMPUTERNAME = os.environ["COMPUTERNAME"]
TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Project root .env
load_dotenv(override=True)
AUTOMATIKDATA_PATH = Path(os.getenv("AUTOMATIKDATA_PATH"))
BRK_PAM_PATH = Path(os.getenv("BRK_PAM_PATH"))
ROBOTUSER = os.getenv("ROBOTUSER")
PROCESS_ID = int(os.getenv("PROCESS_ID"))
ROBOT_DESCRIPTION = os.getenv("ROBOT_DESCRIPTION")

# Automatikdata
load_dotenv(dotenv_path=Path(f"{AUTOMATIKDATA_PATH}/.env"), override=True)
SERVER_PREFIX = os.getenv("SERVER_PREFIX")
TOPDESK_BASE_URL = os.getenv("TOPDESK_BASE_URL")
PROCESS_ID = int(os.getenv("PROCESS_ID"))
DATA_FOLDER_PATH = Path(f"{AUTOMATIKDATA_PATH}/{ROBOTUSER}/data")
LOGS_FOLDER_PATH = Path(f"{AUTOMATIKDATA_PATH}/{ROBOTUSER}/logs")

# Shared pam folder
PAM_PATH_SHARED = Path(f"{BRK_PAM_PATH}/SharedFiles")

# Robot Specific PAM file
PAM_PATH_ROBOT = Path(f"{BRK_PAM_PATH}/{ROBOTUSER}/{ROBOTUSER}.json")

# Read the Topdesk credentials
with open(Path(PAM_PATH_SHARED / "topdesk.json"), "r") as file:
    topdesk_credentials = json.load(file)

# Extract credentials from the JSON data
TD_USERNAME = topdesk_credentials.get("username")
TD_PASSWORD = topdesk_credentials.get("password")

# os2autoproces
# os2autoproces = ApiClient(print_everything=False)

# choose to download or run on already downloaded data
if COMPUTERNAME.startswith(SERVER_PREFIX):
    DOWNLOAD_MODE = 1  # 0 / 1
if DOWNLOAD_MODE == 0:
    SESSION_ID = ROBOTUSER + "_" + "persistent_test_data"
else:
    SESSION_ID = ROBOTUSER + "_" + TIMESTAMP

FOLDER_DATA_SESSION = Path(DATA_FOLDER_PATH / SESSION_ID)

# Logging
LOG_FILE = Path(f"{LOGS_FOLDER_PATH}", f"{TIMESTAMP}.log")

# run only if logger is not already set
# if not any(str(handler._name) == LOG_FILE for handler in logger._core.handlers.values()):
#     logger.add(LOG_FILE, backtrace=True, diagnose=True, catch=True)


def main():
    print("Hejsa, verden!")


if __name__ == "__main__":
    START_TIME = time.time()
    try:
        # if COMPUTERNAME.startswith(SERVER_PREFIX):
        # os2autoproces.update_process(process_id=PROCESS_ID, phase="OPERATION", status="INPROGRESS")

        main()

        # if COMPUTERNAME.startswith(SERVER_PREFIX):
        # os2autoproces.update_process(process_id=PROCESS_ID, phase="OPERATION", status="PENDING")
        END_TIME = time.time()
        DURATION = round(END_TIME - START_TIME)
        logger.info(f"the session took {DURATION} seconds in downloadmode {DOWNLOAD_MODE} on {COMPUTERNAME}")

    except Exception:
        logger.exception("An error occurred.")
        # report to os2autoproces
        if COMPUTERNAME.startswith(SERVER_PREFIX):
            # os2autoproces.update_process(process_id=PROCESS_ID, phase="OPERATION", status="FAILED")
            # report to Topdek
            td_client = Topdeskclient(TOPDESK_BASE_URL, TD_USERNAME, TD_PASSWORD)
            td_client.create_incident(
                request=f"{ROBOTUSER} - {ROBOT_DESCRIPTION} - failed",
                callType="Information",
            )
