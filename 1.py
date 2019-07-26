import json
import time
from enum import Enum, auto


class AccessRoute(Enum):
    DIRECT = auto()
    RAPID = auto()
    PROGRAMME = auto()
    CALIBRATION = auto()
    COMMISSIONING = auto()
    DUTCH = auto()
    RIKEN = auto()
    INDIAN = auto()
    DIRECTORS = auto()
    ICRD = auto()
    COMMERCIAL = auto()
    QENS = auto()
    UNKNOWN = auto()


def parse_access_route_value(access_route_value):
    if not access_route_value or access_route_value in ["Other Time", "Strategic programme", "Special DD"]:
        return AccessRoute.UNKNOWN
    if access_route_value.startswith("Direct Access"):
        return AccessRoute.DIRECT
    if "Programme" in access_route_value:
        return AccessRoute.PROGRAMME
    if "Rapid" in access_route_value:
        return AccessRoute.RAPID
    if "Calibration" == access_route_value:
        return AccessRoute.CALIBRATION
    if "Commissioning" == access_route_value:
        return AccessRoute.COMMISSIONING
    if "Dutch Access" == access_route_value:
        return AccessRoute.DUTCH
    if "Riken Access" == access_route_value:
        return AccessRoute.RIKEN
    if "Indian Access" == access_route_value:
        return AccessRoute.INDIAN
    if "Directors" in access_route_value:
        return AccessRoute.DIRECTORS
    if "Industry Collaboration Research and Development" == access_route_value:
        return AccessRoute.ICRD
    if "Commercial" == access_route_value:
        return AccessRoute.COMMERCIAL
    if "QENS Express" == access_route_value:
        return AccessRoute.QENS
    raise ValueError("Improper Value: " + access_route_value)


def get_digit_access_route(accessroute, round_value):
    simple_access_route_numbers = {
        AccessRoute.RAPID: "0",
        AccessRoute.COMMISSIONING: "30",
        AccessRoute.COMMERCIAL: "5",
        AccessRoute.CALIBRATION: "35",
        AccessRoute.ICRD: "55",
        AccessRoute.INDIAN: "68",
        AccessRoute.DUTCH: "69",
        AccessRoute.RIKEN: "7",
        AccessRoute.QENS: "95",
        AccessRoute.DIRECTORS: "39",
    }

    if accessroute in simple_access_route_numbers.keys():
        return simple_access_route_numbers[accessroute]
    if not round_value:
        return None
    if "_1" in round_value:
        if accessroute is AccessRoute.DIRECT:
            return "1"
        if accessroute is AccessRoute.PROGRAMME:
            return "81"
    elif "_2" in round_value:
        if accessroute is AccessRoute.DIRECT:
            return "2"
        if accessroute is AccessRoute.PROGRAMME:
            return "82"
    return None


def get_year_number(date_submitted):
    epoch_value = entry["Date_Submitted"]
    if epoch_value is None:
        return None
    epoch_value = epoch_value[6:-5]
    year_value = time.strftime("%Y", time.localtime(float(epoch_value)))
    year_value = year_value[-2:]
    return year_value


not_handling = []
successes = []
failures = []

with open("isis.json") as json_file:
    data = json.load(json_file)
numbers = set()
for entry in data:
    accessroute = parse_access_route_value(entry["AccessRouteValue"])
    number = get_digit_access_route(accessroute, entry["Round"])

    if number is None:
        not_handling.append(entry)
        continue
    round_value = entry["Round"]

    if round_value == "RIKEN" and accessroute == AccessRoute.DIRECT:
        year_value = get_year_number(entry["Date_Submitted"])
        if year_value is None:
            not_handling.append(entry)
            continue
    else:
        year_value = entry["Year"]
        year_value = year_value[-2:]
        if year_value == "N/A":
            not_handling.append(entry)
            continue

    if round_value == "Commissioning":
        year_value = get_year_number(entry["Date_Submitted"])
        if year_value is None:
            not_handling.append(entry)
            continue
    else:
        year_value = entry["Year"]
        year_value = year_value[-2:]
        if year_value == "N/A":
            not_handling.append(entry)
            continue

    if accessroute == AccessRoute.RIKEN:
        year_value = get_year_number(entry["Date_Submitted"])
        if year_value is None:
            not_handling.append(entry)
            continue
    else:
        year_value = entry["Year"]
        year_value = year_value[-2:]
        if year_value == "N/A":
            not_handling.append(entry)
            continue

    RB_prefix = year_value + number
    Real_number = entry["RB"]
    if Real_number.startswith(RB_prefix):
        successes.append(entry)
    else:
        failures.append(entry)

with open("not_handling.json", "w") as json_file:
    json.dump(not_handling, json_file)

with open("successes.json", "w") as json_file:
    json.dump(successes, json_file)

with open("failures.json", "w") as json_file:
    json.dump(failures, json_file)

print("Not handling: " + str(len(not_handling)))
print("Successes: " + str(len(successes)))
print("Failures: " + str(len(failures)))
Total = (str(int(len(not_handling)) + int(len(successes)) + int(len(failures))))


class BColours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if int(Total) > len(data):
    print("Total: " + str(Total))
    Colour = BColours.WARNING + BColours.BOLD + BColours.UNDERLINE
    print(Colour, "Error: Something has been duplicated")
    exit()
else:
    print("Total: " + str(Total))
