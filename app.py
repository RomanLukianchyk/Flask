from flask import Flask, request, render_template
from main_functions.CLI import main_cli

app = Flask(__name__)

@app.route('/report')
def show_report():
    order = request.args.get('order', None)
    directory = 'C:/Foxminded/data.t6'
    data = main_cli(files=directory, sort_order=order)
    return render_template('report.html', data=data)


@app.route('/report/driver')
def show_driver():
    driver_id = request.args.get('driver_id')
    directory = 'C:/Foxminded/data.t6'
    data = main_cli(files=directory, driver_name=driver_id)
    return render_template('reports.html', data=data)

@app.route('/driver_list')
def show_driver_list():
    directory = 'C:/Foxminded/data.t6'
    data = main_cli(files=directory, list_drivers=True)
    return render_template('report.html', data=data)


if __name__ == '__main__':
    app.run()
