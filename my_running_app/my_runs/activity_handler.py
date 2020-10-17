import os
import django
from datetime import datetime
from my_runs.garmin import GarminPortal


def create_run_entry():
    gp = GarminPortal()
    # run_data = gp.get_all_summary_activities()
    run_data = gp.get_new_summary_activties((0,3))
    split_data = gp.get_split_of_activities(run_data)

    for run in run_data:
        if run['activityType']['typeKey'] in ['lap_swimming', 'indoor_cycling', 'treadmill_running', 'cycling']:
            continue

        try:
            r, date, activity_id = get_run_data(run)
        except Exception as ex:
            print('There was a problem converting run data')
            print(ex)
            print(activity_id)

        try:
            get_split_data(split_data, r, activity_id, date)

        except Exception as ex:
            print('There was a problem converting run data')
            print(ex)
            print(activity_id)


def get_run_data(run):
    name = run['activityName']
    date = run['startTimeLocal'].split(" ")[0]
    activity_id = run['activityId']
    duration = convert_float_to_datetime(date, run['duration']).timestamp()
    distance = run['distance']

    r = Run(id=activity_id, name=name, date=date, distance=distance, duration=duration)
    r.save()

    return r, date, activity_id


def get_split_data(split_data, r, activity_id, date):
    splits = split_data[activity_id]

    for key, split in splits.items():
        split_number = key
        avg_pace = 0.0 if split['avg_pace'] == '--' else convert_str_to_datetime(date, split['avg_pace']).timestamp()
        s = Split(run=r, split_number=split_number,
                  elapsed_time=convert_str_to_datetime(date, split['elapsed_time']).timestamp(),
                  moving_time=convert_str_to_datetime(date, split['moving_time']).timestamp(),
                  avg_pace=avg_pace)
        s.save()


def convert_str_to_datetime(date: str, time: str):
    time = time.strip()
    date_time = date + " " + time.strip()
    time_format = "%Y-%m-%d %H:%M:%S.%f" if date_time.find(".") != -1 else "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(date_time, time_format)


def convert_float_to_datetime(date: str, float_time: float):
    d = datetime.fromtimestamp(float_time)
    date_time = date + " " + "{}:{}:{}.{}".format(d.hour, d.minute, d.second, d.microsecond)
    return datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")


def diff_between_start_elapsed_time(run):
    import pytz
    from datetime import datetime, timedelta
    start_time = pytz.utc.localize(datetime.strptime(run["startTimeGMT"], "%Y-%m-%d %H:%M:%S"))
    end_time = start_time + timedelta(0, float(run["elapsedDuration"])/1000)
    diff = end_time - start_time
    seconds_in_day = 24 * 60 * 60
    mins, secs = divmod(diff.days * seconds_in_day + diff.seconds, 60)
    #fix this for hours
    return "00:{}:{}".format(mins, secs)


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'my_running_app.settings'
    django.setup()
    from my_runs.models import Run, Split
    create_run_entry()



