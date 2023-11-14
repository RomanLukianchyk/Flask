from pathlib import Path
from main_functions.CLI import main_cli
from flask import Flask, request, render_template, jsonify
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger
import connexion
import xml.etree.ElementTree as ET

app = connexion.FlaskApp(__name__, specification_dir='.')
app.add_api('swagger.yml')

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)


parser = reqparse.RequestParser()
parser.add_argument('version', type=int, help='API version', required=True)
parser.add_argument('format', type=str, help='Response format (JSON, XML)', required=True)


class ReportResource(Resource):
    def get(self):
        version = int(request.args.get('version'))
        format = request.args.get('format')

        if version == 1:
            best_racers, invalid_racers = main_cli(files=Path("data"), sort_order=None)
            if format == 'JSON':
                return jsonify({"best_racers": best_racers, "invalid_racers": invalid_racers})
            elif format == 'XML':
                root = ET.Element("RaceData")

                best_racers_element = ET.Element("BestRacers")
                for racer_key, (formatted_time, full_name, team) in best_racers.items():
                    racer_element = ET.Element("Racer")
                    formatted_time_element = ET.Element("FormattedTime")
                    formatted_time_element.text = formatted_time
                    full_name_element = ET.Element("FullName")
                    full_name_element.text = full_name
                    team_element = ET.Element("Team")
                    team_element.text = team
                    racer_element.append(formatted_time_element)
                    racer_element.append(full_name_element)
                    racer_element.append(team_element)
                    best_racers_element.append(racer_element)

                invalid_racers_element = ET.Element("InvalidRacers")
                for racer_key, (error_message, full_name, team) in invalid_racers.items():
                    racer_element = ET.Element("Racer")
                    error_message_element = ET.Element("ErrorMessage")
                    error_message_element.text = error_message
                    full_name_element = ET.Element("FullName")
                    full_name_element.text = full_name
                    team_element = ET.Element("Team")
                    team_element.text = team
                    racer_element.append(error_message_element)
                    racer_element.append(full_name_element)
                    racer_element.append(team_element)
                    invalid_racers_element.append(racer_element)

                root.append(best_racers_element)
                root.append(invalid_racers_element)

                xml_data = ET.tostring(root, encoding='utf-8')

                response = app.response_class(
                    response=xml_data,
                    status=200,
                    mimetype='application/xml'
                )

                return response

        else:
            return "Unsupported API version"


api.add_resource(ReportResource, '/api/v1/report/')


@app.route('/api/report')
def show_common_report():
    best_racers, invalid_racers = main_cli(files=Path("data"), sort_order=None)
    return render_template('common_report.html', best_racers=best_racers, invalid_racers=invalid_racers)


@app.route('/api/report/drivers')
def show_report():
    order = request.args.get('order', 'asc')
    best_racers, invalid_racers = main_cli(files=Path("data"), sort_order=order)
    return render_template('ordered_report.html', best_racers=best_racers, invalid_racers=invalid_racers)


@app.route('/api/report/driver')
def show_driver():
    driver_id = request.args.get('driver_id')
    best_racers, invalid_racers = main_cli(files=Path("data"), driver_name=driver_id)
    if not driver_id:
        return "Usege: /report/driver?driver_id=SVF"
    return render_template('driver_report.html', best_racers=best_racers, invalid_racers=invalid_racers)


@app.route('/api/driver_list')
def show_driver_list():
    data = main_cli(files=Path("data"), list_drivers=True)
    return render_template('driver_list.html', data=data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
