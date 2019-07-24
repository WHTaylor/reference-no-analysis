import json
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
    if access_route_value and access_route_value in ["Other Time", "Strategic Programme", "Special DD"]:
        return AccessRoute.UNKNOWN
    if access_route_value.startswith("Direct Access"):
        return AccessRoute.DIRECT
    if "Programme" in access_route_value:
        return AccessRoute.PROGRAMME
    if "Rapid" in access_route_value:
        return AccessRoute.RAPID
    if "Calibration" is access_route_value:
        return AccessRoute.CALIBRATION
    if "Commissioning" is access_route_value:
        return AccessRoute.COMMISSIONING
    if "Dutch Access" is access_route_value:
        return AccessRoute.DUTCH
    if "Riken Access" is access_route_value:
        return AccessRoute.RIKEN
    if "Indian Access" is access_route_value:
        return AccessRoute.INDIAN
    if "Directors" in access_route_value:
        return AccessRoute.DIRECTORS
    if "Industry Collaboration Research and Development" is access_route_value:
        return AccessRoute.ICRD
    if "Commercial" is access_route_value:
        return AccessRoute.COMMERCIAL
    if "QENS Express" is access_route_value:
        return AccessRoute.QENS
    raise ValueError("Improper Value: " + access_route_value)

with open("isis-stripped.json") as json_file:
    data = json.load(json_file)
access_route_counts = {}
for entry in data:
    accessroute = parse_access_route_value(entry["AccessRouteValue"])
    if accessroute in access_route_counts.keys():
        access_route_counts[accessroute] = access_route_counts[accessroute] + 1
    else:
        access_route_counts[accessroute] = 1







while True:
    print("NEW REPORT:")
    year = str(input("Which year?"))
    if "0" in (year):
        print()
    if "1" in (year):
        print()
    elif "2" in (year):
        print()
    elif "3" in (year):
        print()
    elif "4" in (year):
        print()
    elif "5" in (year):
        print()
    elif "6" in (year):
        print()
    elif "7" in (year):
        print()
    elif "8" in (year):
        print()
    elif "9" in (year):
        print()
    else:
        print("That is not a year")
        exit()
    sequence_no = "000"
    AR = input("What access route?")
    if AR == "Direct":
        AR_no = str(input("Which round? (integers only) \n October = 1 \n April = 2"))
    elif AR == "Programme":
        AR_no = str(input("Which round? (integers only) \n October = 81 \n April = 82"))
    elif AR == "Rapid":
        AR_no = "0"
    elif AR == "Commissioning":
        AR_no = "30"
    elif AR == "Calibration":
        AR_no = "35"
    elif AR == "Commercial":
        AR_no = "5"
    elif AR == "ICRD":
        AR_no = "55"
    elif AR == "Indian":
        AR_no = "68"
    elif AR == "Dutch":
        AR_no = "69"
    elif AR == "Riken":
        AR_no = "7"
    elif AR == "Xpress":
        AR_no = "9"

    RB = (year[2:]) + (AR_no) + str(sequence_no)

    file = open("data.txt", "a")
    file.write("RB: " + RB + ", Access route: " + AR + "\n")
    file.close()
    print("*Ref no. recorded*")