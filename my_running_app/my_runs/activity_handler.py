import os
import django
import logging
from datetime import datetime
from my_runs.garmin import GarminPortal

os.environ['DJANGO_SETTINGS_MODULE'] = 'my_running_app.settings'
django.setup()
from my_runs.models import Run, Split


def get_data():
    """Pull data from garmin and create django entries"""
    garmin_portal = GarminPortal()
    run_data = garmin_portal.get_summary_activities((0, 30)) # need to find a way of getting new data, not all data
    for run in run_data:
        if run['activityType']['typeKey'] == 'running':
            split_data = garmin_portal.get_splits_of_activity(run['activityId'])
            if split_data:
                create_entry(run, split_data)


def create_entry(run, splits):
    """Create entries for run and associate split data"""
    try:
        run_model = create_run_entry(run)
    except Exception as ex:
        logging.error('There was a problem converting run data for activity id {}'.format(str(run['activityId'])))
        logging.error(ex)
    else:
        try:
            create_split_entry(splits, run_model)
        except Exception as ex:
            logging.error('There was a problem converting split data for activity id {}'.format(str(run['activityId'])))
            logging.error(ex)


def create_run_entry(run):
    """Create run data and save to django db"""
    date = run['startTimeLocal'].split(" ")[0]
    duration = convert_epoch_to_str(run['startTimeLocal'].split(" ")[0], run['duration']).timestamp()
    r = Run(id=run['activityId'], name=run['activityName'], date=date, distance=run['distance'], duration=duration)
    r.save()
    return r


def create_split_entry(splits: dict, run_model):
    """Create split data and save to django db with associated run model"""
    for split_number, split in splits.items():
        elapsed_time = round(split['elapsed_time']/60, 2)
        moving_time = round(split['moving_time']/60, 2)
        s = Split(run=run_model, split_number=split_number,
                  elapsed_time=elapsed_time,
                  moving_time=moving_time)
        s.save()


def convert_epoch_to_str(date: str, float_time: float):
    '''This was a stupid way of doing it, I don't know what I was thinking'''
    d = datetime.fromtimestamp(float_time)
    date_time = date + " " + "{}:{}:{}.{}".format(d.hour, d.minute, d.second, d.microsecond)
    date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
    return date_time


if __name__ == '__main__':
    Run.objects.all().delete()
    Split.objects.all().delete()
    get_data()




