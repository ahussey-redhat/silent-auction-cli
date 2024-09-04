import cli.configuration.variables as app_variables

import schedule

import base64
import datetime
import json
import logging
import threading
import time

class SchedulerInterface(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)

    def run(self):
        logging.debug("Starting token refresh worker")
        schedule.clear()
        schedule.every(60).seconds.do(self.job)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def job(self):
        logging.debug("Checking token expiration")
        access_token_parts = app_variables.TOKEN['access_token'].split('.')
        access_token_payload = json.loads(
            base64.urlsafe_b64decode(
                access_token_parts[1] + '=' * (4 - len(access_token_parts[1]) % 4)
            )
        )
        now = datetime.datetime.now()
        access_token_exp = datetime.datetime.fromtimestamp(access_token_payload['exp'])
        access_token_exp_minus_seconds = access_token_exp - datetime.timedelta(seconds=100)

        if access_token_exp_minus_seconds <= now < access_token_exp:
            logging.debug("Token expired. Refreshing")
            app_variables.TOKEN = app_variables.KC.refresh_token(app_variables.TOKEN)
        else:
            logging.debug("Token still valid")