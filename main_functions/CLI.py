import argparse
import os

from main_functions.building_report import build_report, FoundingDriverError
from main_functions.file_operations import read_abbreviation_file
from main_functions.printing_report import print_report, print_driver_codes_and_names


def main_cli(files, sort_order=None, driver_name=None, list_drivers=False):
    # print(f"Используем папку: {files}")

    try:
        if sort_order is None:
            best_racers, invalid_racers = build_report(files, driver_name=driver_name, sort_order="")
        else:
            best_racers, invalid_racers = build_report(files, driver_name=driver_name, sort_order=sort_order)
    except FileNotFoundError:
        print(f"Ошибка: Один из обязательных файлов не найден")
        return
    except FoundingDriverError as e:
        print(f"Ошибка: {e}")
        return


    if list_drivers:
        abbreviations = read_abbreviation_file(files)
        # print_driver_codes_and_names(abbreviations)
        return abbreviations
    return best_racers, invalid_racers


# def parse_arguments():
#     parser = argparse.ArgumentParser(description="Утилита для обработки отчетов о гонках на автодроме Монако")
#     parser.add_argument("--files", help="Путь к папке с файлами start.txt и end.txt", required=True)
#     parser.add_argument("--asc", action="store_const", const="asc", dest="sort_order", default="asc",
#                         help="Сортировать гонщиков по возрастанию времени (по умолчанию)")
#     parser.add_argument("--desc", action="store_const", const="desc", dest="sort_order",
#                         help="Сортировать гонщиков по убыванию времени")
#     parser.add_argument("--driver", help="Показать статистику о конкретном гонщике")
#
#     return parser.parse_args()


