# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pendulum",
#     "python-dotenv",
#     "loguru",
#     "brkrpautils",
#     "os2apwrapper",
#     "topdeskpy",
# ]
# [tool.uv.sources]
# brkrpautils = { git = "https://github.com/BorholmsRegionsKommuneIT/brkrpautils" }
# os2apwrapper = { git = "https://github.com/BorholmsRegionsKommuneIT/os2apwrapper" }
# topdeskpy = { git = "https://github.com/BorholmsRegionsKommuneIT/topdeskpy" }
# ///


# Hvor logger vi henne? I pakker eller i main?

import os
import time
from pathlib import Path

from dotenv import load_dotenv  # python-dotenv
import pendulum
from loguru import logger
from os2apwrapper import ApiClient
from brkrpautils import get_credentials
from topdeskpy import Topdeskclient

# If using pandas
# pd.set_option("display.max_colwidth", None)


dotenv_path_str = Path("DOTENV_PATH")
with dotenv_path_str.open("r") as file:
    DOTENV_PATH = file.readline().strip()

load_dotenv(DOTENV_PATH, override=True)

COMPUTERNAME = os.environ["COMPUTERNAME"]
USER = os.getenv("USER")
SERVER_PREFIX = os.getenv("SERVER_PREFIX")
FOLDER_PATH = Path(os.getenv("FOLDER_DATA"))
PAM_PATH = Path(os.getenv("PAM_PATH"))
PROCESS_ID = int(os.getenv("PROCESS_ID"))

# Topdesk
TOPDESK_BASE_URL = os.getenv("TOPDESK_BASE_URL")
TD_USERNAME = get_credentials(pam_path=PAM_PATH, user=USER, fagsystem="topdesk")[0]
TD_PASSWORD = get_credentials(pam_path=PAM_PATH, user=USER, fagsystem="topdesk")[1]

# os2autoprocess
autoproces = ApiClient(print_everything=False)

# choose to download or run on already downloaded data
DOWNLOAD_MODE = 0
TIMESTAMP = pendulum.now().strftime("%Y%m%d%H%M%S")

if COMPUTERNAME.startswith(SERVER_PREFIX):
    DOWNLOAD_MODE = 1  # 0 / 1
if DOWNLOAD_MODE == 0:
    SESSION_ID = USER + "_" + "persistent_test_data"
else:
    SESSION_ID = USER + "_" + TIMESTAMP

FOLDER_DATA_SESSION = Path(FOLDER_PATH / SESSION_ID)

# Logging
LOG_FOLDER_PATH = Path(os.getenv("LOG_PATH"))
LOG_FILE = Path(f"{LOG_FOLDER_PATH}", f"{TIMESTAMP}.log")

# run only if logger is not already set

if not any(str(handler._name) == LOG_FILE for handler in logger._core.handlers.values()):
    logger.add(LOG_FILE, backtrace=True, diagnose=True, catch=True)


def main():
    print("Hejsa, verden!")


if __name__ == "__main__":
    START_TIME = time.time()
    try:
        autoproces.update_process(process_id=PROCESS_ID, phase="DEVELOPMENT", status="INPROGRESS")
        if COMPUTERNAME.startswith(SERVER_PREFIX):
            autoproces.update_process(process_id=PROCESS_ID, phase="OPERATION", status="INPROGRESS")

        main()

        autoproces.update_process(process_id=PROCESS_ID, phase="DEVELOPMENT", status="PENDING")
        if COMPUTERNAME.startswith(SERVER_PREFIX):
            autoproces.update_process(process_id=PROCESS_ID, phase="OPERATION", status="PENDING")
        END_TIME = time.time()
        DURATION = round(END_TIME - START_TIME)
        logger.info(f"the session took {DURATION} seconds in downloadmode {DOWNLOAD_MODE} on {COMPUTERNAME}")

    except Exception:
        logger.exception("An error occurred.")
        autoproces.update_process(process_id=PROCESS_ID, phase="DEVELOPMENT", status="FAILED")
        # report to autoproces
        if COMPUTERNAME.startswith(SERVER_PREFIX):
            autoproces.update_process(process_id=PROCESS_ID, phase="OPERATION", status="FAILED")
            # report to Topdek
            td_client = Topdeskclient(TOPDESK_BASE_URL, TD_USERNAME, TD_PASSWORD)
            td_client.create_incident(
                request=f"{USER} with os2autoproces id: {PROCESS_ID} failed",
                callType="Information",
            )
