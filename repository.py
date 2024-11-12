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


class ReportRepository:
    @staticmethod
    def get_common_report():
        return {
            "best_racers": BestRacer.select(),
            "invalid_racers": InvalidRacer.select()
        }

    @staticmethod
    def get_ordered_report(order='asc'):
        if order == 'asc':
            best_racers = BestRacer.select().order_by(BestRacer.formatted_time)
        elif order == 'desc':
            best_racers = BestRacer.select().order_by(BestRacer.formatted_time.desc())
        else:
            best_racers = BestRacer.select()

        return {
            "best_racers": best_racers,
            "invalid_racers": InvalidRacer.select()
        }

    @staticmethod
    def get_driver_list():
        return RacerList.select()

    @staticmethod
    def get_racer_by_id(driver_id):
        try:
            return RacerList.get(RacerList.abbreviation == driver_id)
        except RacerList.DoesNotExist as e:
            raise ValueError(f"Driver not found. Error: {e}")

    @staticmethod
    def get_best_racers_by_full_name(full_name):
        return BestRacer.select().where(BestRacer.full_name == full_name)

    @staticmethod
    def get_invalid_racers_by_full_name(full_name):
        return InvalidRacer.select().where(InvalidRacer.full_name == full_name)
