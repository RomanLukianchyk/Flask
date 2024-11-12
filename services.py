from flask import render_template
from data.database import RacerList, BestRacer, InvalidRacer
from repository import BestRacerRepository, InvalidRacerRepository, ReportRepository


class DriverService:
    @staticmethod
    def get_driver_report(driver_id):
        try:
            mapping = RacerList.get(RacerList.abbreviation == driver_id)
        except RacerList.DoesNotExist as e:
            raise ValueError(f"Водитель не найден. Ошибка: {e}")

        full_name = mapping.full_name
        return {
            "best_racers": BestRacer.select().where(BestRacer.full_name == full_name),
            "invalid_racers": InvalidRacer.select().where(InvalidRacer.full_name == full_name)
        }



class RaceReportService:
    @staticmethod
    def get_best_racers():
        return BestRacerRepository.get_all()

    @staticmethod
    def get_invalid_racers():
        return InvalidRacerRepository.get_all()

    @staticmethod
    def generate_driver_report(request):
        driver_id = request.args.get('driver_id')
        if not driver_id:
            return "Driver ID is required", 400

        try:
            racer_mapping = ReportRepository.get_racer_by_id(driver_id)
            full_name = racer_mapping.full_name

            best_racers = ReportRepository.get_best_racers_by_full_name(full_name)
            invalid_racers = ReportRepository.get_invalid_racers_by_full_name(full_name)

            return render_template('driver_report.html', best_racers=best_racers, invalid_racers=invalid_racers)

        except ValueError as e:
            return str(e), 404
