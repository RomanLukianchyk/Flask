from flask import Flask, request, render_template
from main_functions.CLI import main_cli

app = Flask(__name__)

@app.route('/report')
def show_common_report():
    directory = 'C:/Foxminded/data.t6'
    best_racers, invalid_racers = main_cli(files=directory, sort_order=None)
    return render_template('common_report.html', best_racers=best_racers, invalid_racers=invalid_racers)

@app.route('/report/drivers')
def show_report():
    order = request.args.get('order', 'asc')
    directory = 'C:/Foxminded/data.t6'
    best_racers, invalid_racers = main_cli(files=directory, sort_order=order)
    return render_template('ordered_report.html', best_racers=best_racers, invalid_racers=invalid_racers)

@app.route('/report/driver')
def show_driver():
    driver_id = request.args.get('driver_id')
    directory = 'C:/Foxminded/data.t6'
    best_racers, invalid_racers = main_cli(files=directory, driver_name=driver_id)
    return render_template('driver_report.html', best_racers=best_racers, invalid_racers=invalid_racers)

@app.route('/driver_list')
def show_driver_list():
    directory = 'C:/Foxminded/data.t6'
    data = main_cli(files=directory, list_drivers=True)
    return render_template('driver_list.html', data=data)


if __name__ == '__main__':
    app.run()
