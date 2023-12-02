from peewee import *
from pathlib import Path
from main_functions.CLI import main_cli

db = SqliteDatabase('racers_hub.db')


class BaseModel(Model):
    class Meta:
        database = db


class BestRacer(BaseModel):
    formatted_time = CharField()
    full_name = CharField()
    team = CharField()


class InvalidRacer(BaseModel):
    error_message = CharField()
    full_name = CharField()
    team = CharField()


class RacerList(BaseModel):
    abbreviation = CharField()
    full_name = CharField()


db.connect()
db.create_tables([BestRacer, InvalidRacer, RacerList])


def insert_record_if_not_exists(model_class, condition, **kwargs):
    if not model_class.select().where(condition).exists():
        model_class.create(**kwargs)


def build_models(directory):
    best_racers, invalid_racers = main_cli(files=Path(directory), sort_order=None)
    racer_list = main_cli(files=Path(directory), list_drivers=True)

    for racer_key, (formatted_time, full_name, team) in best_racers.items():
        condition = (BestRacer.full_name == full_name) & (BestRacer.team == team)
        insert_record_if_not_exists(BestRacer, condition, formatted_time=formatted_time, full_name=full_name, team=team)

    for racer_key, (error_message, full_name, team) in invalid_racers.items():
        condition = (InvalidRacer.full_name == full_name) & (InvalidRacer.team == team)
        insert_record_if_not_exists(InvalidRacer, condition, error_message=error_message, full_name=full_name, team=team)

    for abbreviation, (full_name, team) in racer_list.items():
        condition = (RacerList.abbreviation == abbreviation) & (RacerList.full_name == full_name)
        insert_record_if_not_exists(RacerList, condition, abbreviation=abbreviation, full_name=full_name)


build_models('data')


