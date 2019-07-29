import json
import time
from enum import Enum, auto
from typing import Optional, Dict, List


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


simple_access_route_mappings = {
    "Calibration": AccessRoute.CALIBRATION,
    "Commissioning": AccessRoute.COMMISSIONING,
    "Dutch Access": AccessRoute.DUTCH,
    "Riken Access": AccessRoute.RIKEN,
    "Indian Access": AccessRoute.INDIAN,
    "Industry Collaboration Research and Development": AccessRoute.ICRD,
    "Commercial": AccessRoute.COMMERCIAL,
    "QENS Express": AccessRoute.QENS
}

contained_access_route_mappings = {
    "Programme": AccessRoute.PROGRAMME,
    "Rapid": AccessRoute.RAPID,
    "Director": AccessRoute.DIRECTORS
}

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


def parse_access_route_value(access_route_value: str) -> AccessRoute:
    if not access_route_value or access_route_value in ["Other Time", "Strategic programme", "Special DD"]:
        return AccessRoute.UNKNOWN

    if access_route_value.startswith("Direct Access"):
        return AccessRoute.DIRECT

    for route_string, access_route in contained_access_route_mappings.items():
        if route_string in access_route_value:
            return access_route

    if access_route_value in simple_access_route_mappings.keys():
        return simple_access_route_mappings[access_route_value]
    raise ValueError("Improper Value: " + access_route_value)


def get_access_route_number(access_route: AccessRoute, round_value: str) -> Optional[str]:
    if access_route in simple_access_route_numbers.keys():
        return simple_access_route_numbers[access_route]
    if not round_value:
        return None
    if "_1" in round_value:
        if access_route is AccessRoute.DIRECT:
            return "1"
        if access_route is AccessRoute.PROGRAMME:
            return "81"
    elif "_2" in round_value:
        if access_route is AccessRoute.DIRECT:
            return "2"
        if access_route is AccessRoute.PROGRAMME:
            return "82"
    return None


def get_year_from_date_submitted(date_submitted: str) -> Optional[str]:
    if date_submitted is None:
        return None
    epoch_value = date_submitted[6:-5]
    return time.strftime("%Y", time.localtime(float(epoch_value)))


def get_year_number(entry: Dict) -> Optional[str]:
    round_value = entry["Round"]
    if round_value in ["RIKEN", "Commissioning"]:
        year_value = get_year_from_date_submitted(entry["Date_Submitted"])
    else:
        year_value = entry["Year"]

    if not year_value or year_value == "N/A":
        return None
    else:
        return year_value[-2:]


not_handling: List[Dict] = []
successes: List[Dict] = []
failures: List[Dict] = []

with open("isis.json") as json_file:
    data: List[Dict] = json.load(json_file)

for entry in data:
    access_route: AccessRoute = parse_access_route_value(entry["AccessRouteValue"])
    number: Optional[str] = get_access_route_number(access_route, entry["Round"])

    if number is None:
        not_handling.append(entry)
        continue

    year_number: Optional[str] = get_year_number(entry)
    if year_number is None:
        not_handling.append(entry)
        continue

    rb_prefix: str = year_number + number
    actual_rb: str = entry["RB"]
    if actual_rb.startswith(rb_prefix):
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
