import os
import datetime
import sys
from main_functions.config import DATETIME_FORMAT


class FilesEmpty(Exception):
    def __init__(self, message="Файл пуст или не содержит записей."):
        super().__init__(message)


class InvalidAbbreviationError(Exception):
    def __init__(self, message="Неправильная аббревиатура в файле abbreviation.txt"):
        super().__init__(message)
        print(message)
        sys.exit(1)


def read_file_values(file_path):
    values = {}
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if not lines:
                raise FilesEmpty()
            for line in lines:
                line = line.strip()
                if line:
                    racer_id, racer_datetime = parse_racer_line(line)
                    if racer_id not in values:
                        values[racer_id] = racer_datetime
                    else:
                        if racer_datetime < values[racer_id]:
                            values[racer_id] = racer_datetime
    except FileNotFoundError as e:
        raise e

    return values


def read_file_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines


def parse_racer_line(line):
    racer_id = line[:3]
    racer_date = line[3:13]
    racer_time = line[14:]
    datetime_string = racer_date + '_' + racer_time
    racer_datetime = datetime.datetime.strptime(datetime_string, DATETIME_FORMAT)
    return racer_id, racer_datetime


def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return content


def get_full_file_path(directory, file_name):
    full_file_path = os.path.join(directory, file_name)
    return full_file_path


def read_abbreviation_file(directory):
    abbreviations_path = get_full_file_path(directory, "abbreviations.txt")
    abbreviations = {}

    for line in read_file_lines(abbreviations_path):
        line = line.strip()
        if line:
            abbreviation, full_name, team = line.split('_')
            if not is_valid_abbreviation(abbreviation):
                raise InvalidAbbreviationError()
            abbreviations[abbreviation] = (full_name, team)

    return abbreviations


def is_valid_abbreviation(abbreviation):
    return abbreviation[:3].isalpha() and abbreviation[:3].isupper()


def read_start_file(directory):
    start_path = get_full_file_path(directory, "start.txt")
    try:
        return read_file_values(start_path)
    except FilesEmpty as e:
        print(e)
        sys.exit(1)


def read_end_file(directory):
    end_path = get_full_file_path(directory, "end.txt")
    try:
        return read_file_values(end_path)
    except FilesEmpty as e:
        print(e)
        sys.exit(1)
