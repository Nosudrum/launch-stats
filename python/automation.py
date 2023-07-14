import json
import os

import requests

from ImportAll import import_all_data, header
from plots import generate_plots

LAST_LAUNCH_URL = "https://ll.thespacedevs.com/2.2.0/launch/previous/?limit=1&status__ids=3,4,7&mode=list"


def get_last_launch():
    print("Getting last launch...")
    last_launch = requests.get(LAST_LAUNCH_URL, headers=header, timeout=1440).json()
    return (
        last_launch["results"][0],
        last_launch["results"][0]["id"],
        last_launch["results"][0]["status"]["id"],
    )


def get_cached_last_launch():
    print("Getting cached last launch...")
    with open("cache/last_launch.json", "r") as file:
        last_launch = json.load(file)
    return last_launch["id"], last_launch["status"]["id"]


def update_cache(launch):
    print("Updating cache...")
    with open("cache/last_launch.json", "w") as file:
        json.dump(launch, file, indent=4)


if __name__ == "__main__":
    launch, new_id, new_status = get_last_launch()
    if os.path.exists("cache/last_launch.json"):
        old_id, old_status = get_cached_last_launch()
        if new_id == old_id and new_status == old_status:
            print("Latest launch has not changed. No need to update.")
            exit(code=0)
    update_cache(launch)
    import_all_data()
    generate_plots(show=False)
    exit(code=0)
