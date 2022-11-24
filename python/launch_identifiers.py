from datetime import timedelta, datetime

from Processing import PastStatus, PastT0s, PastName
import pandas as pd
import requests

PastT0s = PastT0s.copy()
PastStatus = PastStatus.copy().rename(columns={"id": "status_id", "abbrev": "status_name"})
PastName = PastName.copy()

data = pd.concat([PastT0s, PastStatus[["status_id", "status_name"]], PastName], axis=1)

year_selected = 2001

data_year = data[data.net.dt.year == year_selected].copy().reset_index(drop=True)


def get_celestrak_data(identifier_):
    print(f'Getting data for {identifier_}')
    URL = f'https://celestrak.com/satcat/records.php?INTDES={identifier_}'
    celestrak_json = requests.get(URL, timeout=360).json()
    return celestrak_json[0]["OBJECT_NAME"], celestrak_json[0]["LAUNCH_DATE"]


def cleanup_string(string_):
    cleaned_string = ''
    for char in string_.lower():
        if char.isalpha():
            cleaned_string += char
        else:
            cleaned_string += ' '
    return cleaned_string


def name_match(string1, string2):
    string1 = set(cleanup_string(string1).replace("kosmos", "cosmos").split())
    string2 = set(cleanup_string(string2).replace("kosmos", "cosmos").split())
    if string1 & string2:
        return True
    else:
        return False


def set_identifier_match(index, identifier_, name_):
    print(f'Found match for {data_year.loc[index, "name"]} ({data_year.loc[index, "status_name"]})')
    data_year.loc[i, "identifier"] = identifier_
    data_year.loc[i, "name_check"] = name_


def set_identifier_none(index):
    print(f'No match for {data_year.loc[index, "name"]} ({data_year.loc[index, "status_name"]})')
    data_year.loc[i, "identifier"] = None
    data_year.loc[i, "name_check"] = None


count = 0
for i in data_year.index:
    count += 1
    identifier = f'{data_year.loc[i, "net"].strftime("%Y")}-{count:03d}A'
    name, date = get_celestrak_data(identifier)
    if data_year.loc[i, "net"] - timedelta(days=3) <= datetime.strptime(date + "+00:00", "%Y-%m-%d%z") <= \
            data_year.loc[i, "net"] + timedelta(days=3):
        # Check if identifier launch date roughly matches launch date
        if data_year.loc[i, "status_id"] == 4:
            # If launch failure, make sure name matches
            if name_match(name, data_year.loc[i, "name"]):
                # Name matches, so failed launch has an identifier
                set_identifier_match(i, identifier, name)
            else:
                # Name does not match, so failed launch does not have an identifier
                set_identifier_none(i)
                count -= 1
        else:
            # If launch success, check various things
            if name_match(name, data_year.loc[i, "name"]):
                # If name matches, assign this identifier to the launch
                set_identifier_match(i, identifier, name)
            elif (i < data_year.tail(1).index.values.item()) and (
                    data_year.loc[i, "net"].strftime("%Y-%m-%d") == data_year.loc[i + 1, "net"].strftime("%Y-%m-%d")) \
                    and name_match(name, data_year.loc[i + 1, "name"]):
                # There is another launch on the same day corresponding to the identifier
                set_identifier_none(i)
                count -= 1
            else:
                # Assign this identifier to the launch
                set_identifier_match(i, identifier, name)
    else:
        # If launch date does not match, then no identifier for this launch
        set_identifier_none(i)
        count -= 1

print("Done")
