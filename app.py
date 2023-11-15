from pathlib import Path
from main_functions.CLI import main_cli
from flask import Flask, request, render_template, jsonify
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger
import xml.etree.ElementTree as ET

app = Flask(__name__)
api = Api(app)
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Race Report API",
        "description": "API for accessing race report data",
        "version": "0.0.1"
    },
}

swagger = Swagger(app, template=swagger_template)

parser = reqparse.RequestParser()
parser.add_argument('version', type=int, help='API version', required=True)
parser.add_argument('format', type=str, help='Response format (JSON, XML)', required=True)


class ReportResource(Resource):
    def get(self):
        """
        Get Race Report
        ---
        tags:
          - Report
        parameters:
          - name: version
            in: query
            type: integer
            required: true
            description: API version (e.g., 1)
          - name: format
            in: query
            type: string
            required: true
            description: Response format (JSON, XML)
        responses:
          '200':
            description: Successful response
            schema:
              type: object
              properties:
                best_racers:
                  type: object
                  description: Best racers data
                invalid_racers:
                  type: object
                  description: Invalid racers data
          '400':
            description: Bad Request
        """
        version = int(request.args.get('version', 1))
        format = request.args.get('format', 'JSON')

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


@app.route('/report')
def show_common_report():
    """
    Show Common Report
    ---
    tags:
      - Report
    summary: Show Common Report
    description: This endpoint renders a common HTML report.
    responses:
      '200':
        description: Successful response
    parameters:
      - name: order
        in: query
        type: string
        required: false
        description: Order for the report (asc, desc)
    """
    best_racers, invalid_racers = main_cli(files=Path("data"), sort_order=None)
    return render_template('common_report.html', best_racers=best_racers, invalid_racers=invalid_racers)


@app.route('/report/drivers')
def show_report():
    """
    Show Report
    ---
    tags:
      - Report
    summary: Show Report
    description: This endpoint renders an ordered HTML report.
    responses:
      '200':
        description: Successful response
    parameters:
      - name: order
        in: query
        type: string
        required: false
        description: Order for the report (asc, desc)
    """
    order = request.args.get('order', 'asc')
    best_racers, invalid_racers = main_cli(files=Path("data"), sort_order=order)
    return render_template('ordered_report.html', best_racers=best_racers, invalid_racers=invalid_racers)


@app.route('/report/driver')
def show_driver():
    """
    Show Driver Report
    ---
    tags:
      - Report
    summary: Show Driver Report
    description: This endpoint renders an HTML report for a specific driver.
    responses:
      '200':
        description: Successful response
    parameters:
      - name: driver_id
        in: query
        type: string
        required: false
        description: Driver ID (e.g., SVF)
    """
    driver_id = request.args.get('driver_id')
    best_racers, invalid_racers = main_cli(files=Path("data"), driver_name=driver_id)
    if not driver_id:
        return "Usege: /report/driver?driver_id=SVF"
    return render_template('driver_report.html', best_racers=best_racers, invalid_racers=invalid_racers)


@app.route('/driver_list')
def show_driver_list():
    """
    Show Driver List
    ---
    tags:
      - Report
    summary: Show Driver List
    description: This endpoint renders a list of drivers in HTML.
    responses:
      '200':
        description: Successful response
    """
    data = main_cli(files=Path("data"), list_drivers=True)
    return render_template('driver_list.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
