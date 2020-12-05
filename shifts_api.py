from flask import Flask, request, jsonify

from lib.date_utils import previous_week_monday, previous_week_friday
from lib.random_shift_data import User, Timesheet

app = Flask(__name__)


@app.route('/users', methods=['GET'])
def users():
    all_users = User.get_all_users()
    return jsonify(all_users)


@app.route('/previous_week_shifts', methods=['GET'])
def previous_week_shifts():
    user_ids = request.args.get('user_ids')
    if user_ids:
        try:
            user_ids = [int(user_id) for user_id in user_ids.split(',')]
        except ValueError:
            return 'Bad Request - user_ids could not be parsed!', 400
    else:
        user_ids = [user['id'] for user in User.get_all_users()]

    shifts = []
    for user_id in user_ids:
        timesheet = Timesheet(
            user_id,
            previous_week_monday(),
            previous_week_friday()
        )
        timesheet.generate_random_shifts()
        shifts += timesheet.shifts

    return jsonify(shifts)
