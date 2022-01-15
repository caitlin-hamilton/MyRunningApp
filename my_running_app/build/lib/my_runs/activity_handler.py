import os
import django
import math
import logging
import pytz
from datetime import datetime, timedelta
from my_runs.garmin import GarminPortal

logging.basicConfig(level=logging.DEBUG)


def get_data_from_garmin():
    garmin_portal = GarminPortal()
    run_data = garmin_portal.get_summary_activities((0, 3))
    for run in run_data:
        split_data = garmin_portal.get_splits_of_activity(run['activityId'])

    return run_data, split_data


def create_run_entry(run_data, split_data):

    for run in run_data:
        if not run.get('activityType', None) and run['activityType']['typeKey'] in ['lap_swimming', 'indoor_cycling',
                                                                                    'treadmill_running', 'cycling']:
            continue

        try:
            run_model = get_run_data(run)
        except Exception as ex:
            logging.error('There was a problem converting run data for activity id {}'.format(str(run_model.id)))
            logging.error(ex)

        try:
            get_split_data(split_data, run_model)

        except Exception as ex:
            logging.error('There was a problem converting split data for activity id {}'.format(str(run_model.id)))
            logging.error(ex)


def get_run_data(run):
    date = run['startTimeLocal'].split(" ")[0]
    activity_id = run['activityId']
    duration = convert_float_to_datetime(date, run['duration']).timestamp()

    r = Run(id=activity_id, name=run['activityName'], date=date, distance=run['distance'], duration=duration)
    r.save()

    return r


def get_split_data(split_data, run_model):
    splits = split_data[run_model.id]
    if not len(splits) == math.ceil(run_model.distance/1000):
        #some of my splits don't equal 1km because I pressed the wrong button on my watch
        #this means the data isn't valid, so just delete it and skip
        run_model.delete()
        return

    for key, split in splits.items():
        split_number = key
        avg_pace = 0.0 if split['avg_pace'] == '--' else convert_str_to_datetime(run_model.date, split['avg_pace']).timestamp()
        s = Split(run=run_model, split_number=split_number,
                  elapsed_time=convert_str_to_datetime(run_model.date, split['elapsed_time']).timestamp(),
                  moving_time=convert_str_to_datetime(run_model.date, split['moving_time']).timestamp(),
                  avg_pace=avg_pace)
        s.save()


def convert_str_to_datetime(date: str, time: str):
    date_time = date + " " + time.strip()
    time_format = "%Y-%m-%d %H:%M:%S.%f" if date_time.find(".") != -1 else "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(date_time, time_format)


def convert_float_to_datetime(date: str, float_time: float):
    d = datetime.fromtimestamp(float_time)
    date_time = date + " " + "{}:{}:{}.{}".format(d.hour, d.minute, d.second, d.microsecond)
    date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
    return date_time


def diff_between_start_elapsed_time(run):
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

    run_data, split_data = get_data_from_garmin()
    create_run_entry(run_data, split_data)



