from data.database import BestRacer, InvalidRacer, RacerList


class BestRacerRepository:
    @staticmethod
    def create(formatted_time, full_name, team):
        return BestRacer.create(
            formatted_time=formatted_time, full_name=full_name, team=team)

    @staticmethod
    def get_all():
        return BestRacer.select()


class InvalidRacerRepository:
    @staticmethod
    def create(formatted_time, full_name, team):
        return InvalidRacer.create(
            formatted_time=formatted_time, full_name=full_name, team=team)

    @staticmethod
    def get_all():
        return InvalidRacer.select()


class RacerListRepository:
    @staticmethod
    def create(abbreviation, full_name):
        return RacerList.create(abbreviation=abbreviation, full_name=full_name)

    @staticmethod
    def get_all():
        return RacerList.select()


class RaceReportService:
    @staticmethod
    def get_best_racers():
        return BestRacerRepository.get_all()

    @staticmethod
    def get_invalid_racers():
        return InvalidRacerRepository.get_all()