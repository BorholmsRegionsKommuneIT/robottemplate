import time
import json
from pathlib import Path

# from os2apwrapper import ApiClient
from topdeskpy import Topdeskclient
from opuspy import say_hello_from_opuspy
from config import Config

# init config and logger
config = Config(download_mode=0, sample_mode=0)
logger = config.logger

# Read Topdesk credentials
with open(Path(f"{config.PAM_PATH_SHARED}/topdesk.json"), "r") as file:
    topdesk_credentials = json.load(file)
TD_USERNAME = topdesk_credentials.get("username")
TD_PASSWORD = topdesk_credentials.get("password")
td_client = Topdeskclient(config.TOPDESK_BASE_URL, TD_USERNAME, TD_PASSWORD)

# run only if logger is not already set
# if not any(str(handler._name) == LOG_FILE for handler in logger._core.handlers.values()):
#     logger.add(LOG_FILE, backtrace=True, diagnose=True, catch=True)


def main():
    say_hello_from_opuspy()
    logger.info("Starting the script")


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
        logger.info(f"the session took {DURATION} seconds in downloadmode {config.DOWNLOAD_MODE} on {config.COMPUTERNAME}")

    except Exception:
        logger.exception("An error occurred.")
        # report to os2autoproces
        if config.COMPUTERNAME.startswith(config.SERVER_PREFIX):
            # os2autoproces.update_process(process_id=PROCESS_ID, phase="OPERATION", status="FAILED")
            # report to Topdek
            td_client.create_incident(
                request=f"{config.ROBOTUSER} - {config.ROBOT_DESCRIPTION} - failed",
                callType="Information",
            )
