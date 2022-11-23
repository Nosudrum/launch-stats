from Processing import PastStatus, PastT0s, PastName
import pandas as pd
import requests

PastT0s = PastT0s.copy()
PastStatus = PastStatus.copy().rename(columns={"id": "status_id", "abbrev": "status_name"})
PastName = PastName.copy()

data = pd.concat([PastT0s, PastStatus[["status_id", "status_name"]], PastName], axis=1)

year_selected = 2019

data_year = data[data.net.dt.year == year_selected].copy()


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
    string1 = set(cleanup_string(string1).split())
    string2 = set(cleanup_string(string2).split())
    if string1 & string2:
        return True
    else:
        return False


count = 0
for i in data_year.index:
    count += 1
    if data_year.loc[i, "status_id"] == 3 or data_year.loc[i, "status_id"] == 7:  # Success or partial failure
        identifier = f'{data_year.loc[i, "net"].strftime("%Y")}-{count:03d}A'
        name, date = get_celestrak_data(identifier)
        if date == data_year.loc[i, "net"].strftime("%Y-%m-%d"):
            print(f'Found match for {data_year.loc[i, "name"]} ({data_year.loc[i, "status_name"]})')
            data_year.loc[i, "identifier"] = identifier
            data_year.loc[i, "name_check"] = name
        else:
            print(f'No match for {data_year.loc[i, "name"]} ({data_year.loc[i, "status_name"]})')
            data_year.loc[i, "identifier"] = None
            data_year.loc[i, "name_check"] = None
            count -= 1
    else:
        identifier_1 = f'{data_year.loc[i, "net"].strftime("%Y")}-{count:03d}A'
        identifier_2 = f'{data_year.loc[i, "net"].strftime("%Y")}-{(count + 1):03d}A'
        name_1, date_1 = get_celestrak_data(identifier_1)
        name_2, date_2 = get_celestrak_data(identifier_2)
        if date_1 == date_2:
            if name_match(data_year.loc[i, "name"], name_1):
                print(f'Found match for {data_year.loc[i, "name"]} ({data_year.loc[i, "status_name"]})')
                data_year.loc[i, "identifier"] = identifier_1
                data_year.loc[i, "name_check"] = name_1
            elif name_match(data_year.loc[i, "name"], name_2):
                print(f'Found match for {data_year.loc[i, "name"]} ({data_year.loc[i, "status_name"]})')
                data_year.loc[i, "identifier"] = identifier_2
                data_year.loc[i, "name_check"] = name_2
            else:
                print(f'No match for {data_year.loc[i, "name"]} ({data_year.loc[i, "status_name"]})')
                data_year.loc[i, "identifier"] = None
                data_year.loc[i, "name_check"] = None
                count -= 1
        else:
            print(f'No match for {data_year.loc[i, "name"]} ({data_year.loc[i, "status_name"]})')
            data_year.loc[i, "identifier"] = None
            data_year.loc[i, "name_check"] = None
            count -= 1

print("Done")
