import json
import os

import requests

from ImportAll import import_all_data, header

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
    if not os.path.exists("cache"):
        os.mkdir("cache")
    if not os.path.exists("cache/last_launch.json"):
        file = open("cache/last_launch.json", "x")
    else:
        file = open("cache/last_launch.json", "w")
    json.dump(launch, file, indent=4)
    file.close()


if __name__ == "__main__":
    launch, new_id, new_status = get_last_launch()
    if os.path.exists("cache/last_launch.json"):
        old_id, old_status = get_cached_last_launch()
        if new_id == old_id and new_status == old_status:
            print("Latest launch has not changed. No need to update.")
            exit(code=0)
        else:
            print("Latest launch has changed. Updating all plots.")
    else:
        print("Cache does not exist. Creating and updating all plots.")
    update_cache(launch)
    import_all_data()
    from plots import generate_plots

    generate_plots(show=False)
    exit(code=0)
