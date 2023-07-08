"""The main handler function which sends a stock report to discord"""

import os
from time import perf_counter
from datetime import datetime
import json
from base64 import b64decode

import fire

from google.cloud.exceptions import NotFound

from discord_webhook import DiscordWebhook

# pylint: disable=import-error
from utils.utils import list_all_jpg_from_gcs, get_jpg_from_bucket, check_date_format

BUCKET = os.environ["BUCKET"]
WEBHOOK = os.environ["WEBHOOK"]

#############
## Handler ##
#############


def main(event=None, context=None):
    """Handler function which sends reports/notifications to discord"""

    if set(event.keys()) == {"date"}:  # Invoked manually.
        pass
    else:  # Invoked via pubsub.
        event = json.loads(b64decode(event["data"]).decode("utf-8"))

    date = event.get("date", datetime.today().strftime('%Y%m%d'))
    check_date_format(date)

    webhook = DiscordWebhook(url=WEBHOOK)

    files = [i for i in list_all_jpg_from_gcs(BUCKET) if i[11:15] == date[4:]] 

    for file in sorted(files, key=lambda x: x.split("/")[-1]):
        try:
            file_content = get_jpg_from_bucket(BUCKET, file)
        except NotFound:
            print(file, "not found")
            continue

        webhook.add_file(file=file_content, filename=file)

    # Execute
    webhook.execute()
    print("Flashback created and sent successfully!")


##########
## Main ##
##########

if __name__ == "__main__":
    start = perf_counter()
    fire.Fire(main)
    print(f"Execution time: {perf_counter() - start:.2f} seconds")
