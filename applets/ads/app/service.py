"""
# Ads Applet Service

Based on mediaPanel data format version 6

What It Do:

This is a service designed for generating an "ads_report.json" in an Applet
directory, which will be used for generating a report on what ads are coming
up and what ads are going to go out of date.
"""

import glob
import itertools
import logging
from datetime import date, datetime, timedelta
from os import listdir
from os.path import join

from mediapanel.applets import StorageManager
from mediapanel.config.ads import (AdsConfig, AdsVerticalConfig,
                                   AdsHorizontalConfig)
from mediapanel.timedelta import human_readable

logging.basicConfig(level=logging.DEBUG)


def readable_time_until(now: datetime, then: date):
    """
    Use a mediaPanel utility function to generate a human-readable
    representation of how long until an event happens.
    """
    then_datetime = datetime(year=then.year, month=then.month, day=then.day)
    td = abs(now - then_datetime)

    return human_readable(td)


# Find files for ad configs
BASE = "/resources"
HOMEDIR = "home/mediapanel/themes/displayAD"
ADS_TYPES = ["adConfig", "adConfig_horizontal", "adConfig_vertical"]

# Loop through files and categorize into upcoming and expired
upcoming_ads = {}
expiring_ads = {}
today = date.today()
now = datetime.now()

# TODO DOING: rewrite loop to go through all clients, and then go through all
# globs in THAT directory

ads_mgr = StorageManager("media_scheduler", "index")

for client_id_str in listdir(BASE):
    if not client_id_str.isnumeric():
        continue
    logging.debug("Working for client #%s", client_id_str)
    client_id = int(client_id_str)
    upcoming = []
    expiring = []

    # Setting up where to search for files
    # -- Device files
    # 1/*/home/mediapanel/themes/displayAD/adConfig.json
    # 1/*/home/mediapanel/themes/displayAD/adConfig_horizontal.json
    # 1/*/home/mediapanel/themes/displayAD/adConfig_vertical.json
    # -- Group files
    # */home/mediapanel/themes/displayAD/adConfig.json
    # */home/mediapanel/themes/displayAD/adConfig_horizontal.json
    # */home/mediapanel/themes/displayAD/adConfig_vertical.json
    BASE_PATH = join(BASE, client_id_str)
    USER_PATH = [join(BASE_PATH, "1", "*", HOMEDIR, ads_type + ".json")
                 for ads_type in ADS_TYPES]
    GROUP_PATH = [join(BASE_PATH, "*", HOMEDIR, ads_type + ".json")
                  for ads_type in ADS_TYPES]
    logging.debug("%r", USER_PATH)
    logging.debug("%r", GROUP_PATH)
    matched_files = [glob.iglob(user_path)
                     for user_path in USER_PATH]
    matched_files += [glob.iglob(group_path)
                      for group_path in GROUP_PATH]
    for filename in itertools.chain(*matched_files):
        logging.debug("Loading file: %r", filename)
        try:
            # Load advertisements for specific type
            if "vertical" in filename:
                ads_config = AdsVerticalConfig.from_v6_file(filename)
            elif "horizontal" in filename:
                ads_config = AdsHorizontalConfig.from_v6_file(filename)
            else:
                ads_config = AdsConfig.from_v6_file(filename)

            # Loop through advertisements and find upcoming or expiring
            for ad in ads_config.ads:
                start_time = ad.timeframe.start_day
                start_day = start_time.date()
                end_time = ad.timeframe.end_day
                end_day = end_time.date()
                if timedelta(days=0) > today - start_day > timedelta(days=-4):
                    upcoming.append({
                        "name": ad.name,
                        "link": "#",
                        "time_left": readable_time_until(now, start_time)})
                elif timedelta(days=5) > end_day - today > timedelta(days=0):
                    upcoming.append({
                        "name": ad.name,
                        "link": "#",
                        "time_left": readable_time_until(now, end_time)})

            logging.debug("Saving ads for client: %r", client_id)
            # Store upcoming and expiring advertisements to file
            ads_mgr.save({"upcoming": upcoming, "expiring": expiring},
                         client_id)

        except IOError as e:
            logging.error("IOError with file %r: %r", filename, e)
        except Exception as e:
            logging.error("Generic exception with file %r: %r", filename, e)
