import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv  # python-dotenv
import pendulum
from loguru import logger
from os2apwrapper import ApiClient
from brkrpautils import get_credentials, TOPdeskIncidentClient

# If using pandas
# pd.set_option("display.max_colwidth", None)
sys.dont_write_bytecode = True
dotenv_path_str = Path("DOTENV_PATH")

with dotenv_path_str.open("r") as file:
    DOTENV_PATH = file.readline().strip()

load_dotenv(DOTENV_PATH, override=True)

COMPUTERNAME = os.environ["COMPUTERNAME"]
USER = os.getenv("USER")
SERVER_PREFIX = os.getenv("SERVER_PREFIX")
FOLDER_PATH = Path(os.getenv("FOLDER_DATA"))
SAPSHCUT_PATH = Path(os.getenv("SAPSHCUT_PATH"))
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

if not any(
    str(handler._name) == LOG_FILE for handler in logger._core.handlers.values()
):
    logger.add(LOG_FILE, backtrace=True, diagnose=True, catch=True)


def main():
    result = 1 + 1
    print(result)


if __name__ == "__main__":
    try:
        START_TIME = time.time()
        if COMPUTERNAME.startswith(SERVER_PREFIX):
            autoproces.update_process(
                process_id=PROCESS_ID, phase="OPERATION", status="INPROGRESS"
            )
        else:
            autoproces.update_process(
                process_id=PROCESS_ID, phase="DEVELOPMENT", status="INPROGRESS"
            )
        main()
        if COMPUTERNAME.startswith(SERVER_PREFIX):
            autoproces.update_process(
                process_id=PROCESS_ID, phase="OPERATION", status="PENDING"
            )
        else:
            autoproces.update_process(
                process_id=PROCESS_ID, phase="DEVELOPMENT", status="PENDING"
            )
        END_TIME = time.time()
        DURATION = round(END_TIME - START_TIME)
        logger.info(
            f"the session took {DURATION} seconds in downloadmode {DOWNLOAD_MODE} on {COMPUTERNAME}"
        )
    except Exception:
        logger.exception("An error occurred.")
        # report to autoproces
        if COMPUTERNAME.startswith(SERVER_PREFIX):
            autoproces.update_process(
                process_id=PROCESS_ID, phase="OPERATION", status="FAILED"
            )
            # report to Topdek
            td_client = TOPdeskIncidentClient(
                TOPDESK_BASE_URL, TD_USERNAME, TD_PASSWORD
            )
            td_client.create_incident(
                request=f"{USER} with os2autoproces id: {PROCESS_ID} failed"
            )
            autoproces.update_process(
                process_id=PROCESS_ID, phase="DEVELOPMENT", status="FAILED"
            )
