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
import json
import logging
from datetime import date, datetime, timedelta

from mediapanel.config.ads import (AdsConfig, AdsVerticalConfig,
                                   AdsHorizontalConfig)

logging.basicConfig(level=logging.DEBUG)


def readable_time_until(now: datetime, then: date):
    """
    Create a representation of how long until a time is reached. Will generate
    a string with reasonable breaks at "60 minutes" => "1 hour", "24 hours" =>
    "1 day". Does not need anything higher as this script doesn't go past 5
    days.
    """
    then_datetime = datetime(year=then.year, month=then.month, day=then.day)
    td = abs(now - then_datetime)

    if td.days:
        # Days
        if td.days == 1:
            return "1 day"
        else:
            return f"{td.days} days"
    elif td.seconds > 60 * 60:
        # Hours
        if td.seconds // (60 * 60) < 2:
            return "1 hour"
        else:
            return f"{td.seconds // (60 * 60)} hours"
    # Minutes; "1 minutes" case is so rare I don't care about it
    return f"{td.seconds // 60} minutes"


# Find files for ad configs
base = "/resources"
homedir = "home/mediapanel/themes/displayAD"
ads_types = ["adConfig", "adConfig_horizontal", "adConfig_vertical"]
matched_files = [
    glob.iglob("%s/*/1/*/%s/%s.json" % (base, homedir, ads_type))
    for ads_type in ads_types]
matched_files += [
    glob.iglob("%s/*/*/%s/group*_%s.json" % (base, homedir, ads_type))
    for ads_type in ads_types]

# Loop through files and categorize into upcoming and expired
upcoming_ads = {}
expiring_ads = {}
today = date.today()
now = datetime.now()

for filename in itertools.chain(*matched_files):
    client_id = filename.split("/")[2]
    c_upcoming = upcoming_ads[client_id] = upcoming_ads.get(client_id, [])
    c_expiring = expiring_ads[client_id] = expiring_ads.get(client_id, [])
    logging.debug("Storing under client: %s", client_id)
    try:
        logging.debug("Loading ads from file: %s", filename)
        if "vertical" in filename:
            ads_config = AdsVerticalConfig.from_v6_file(filename)
        elif "horizontal" in filename:
            ads_config = AdsHorizontalConfig.from_v6_file(filename)
        else:
            ads_config = AdsConfig.from_v6_file(filename)
        for ad in ads_config.ads:
            start_day = ad.timeframe.start_day.date()
            end_day = ad.timeframe.end_day.date()
            if timedelta(days=0) > today - start_day > timedelta(days=-4):
                c_upcoming.append({
                    "name": ad.name,
                    "link": "#",
                    "time_left": readable_time_until(now,
                                                     ad.timeframe.start_day)})
            elif timedelta(days=5) > end_day - today > timedelta(days=0):
                c_expiring.append({
                    "name": ad.name,
                    "link": "#",
                    "time_left": readable_time_until(now,
                                                     ad.timeframe.end_day)})
    except Exception as e:
        logging.error("Found error with file: %s", filename)
        logging.error("Error: %r", str(e))

with open("/applets/ads_report.json", "w") as f:
    output = {
        "expiring": expiring_ads,
        "upcoming": upcoming_ads,
        }
    logging.debug("%r", output)
    json.dump(output, f)
