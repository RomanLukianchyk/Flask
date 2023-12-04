from flask import render_template
from repository import BestRacerRepository, InvalidRacerRepository, ReportRepository


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
