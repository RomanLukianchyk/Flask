import sys
from main_functions.config import NUM_TOP_RACERS


def format_racer_info(index, full_name, team, time):
    return f"{index}. {full_name.ljust(20)} | {team.ljust(30)}| {time}"

def print_driver_codes_and_names(abbreviations):
    print("Список имен и кодов водителей:")
    for driver_key, (full_name, _) in abbreviations.items():
        print(f"{driver_key} {full_name}")


def print_report(report):
    if not report:
        print("Список пуст.")
        sys.exit()

    report_list = list(report.items())

    for index, (driver_key, (time, full_name, team)) in enumerate(report_list[:NUM_TOP_RACERS], start=1):
        full_name = full_name if full_name else ""
        team = team if team else ""

        line = format_racer_info(index, full_name, team, time)
        print(line)

    if len(report_list) > NUM_TOP_RACERS:
        print("_" * 80)

        for index, (driver_key, (time, full_name, team)) in enumerate(report_list[NUM_TOP_RACERS:], start=NUM_TOP_RACERS):
            full_name = full_name if full_name else ""
            team = team if team else ""

            line = format_racer_info(index, full_name, team, time)
            print(line)
