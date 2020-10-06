from django.shortcuts import render, get_object_or_404
import pytz
from django.http import HttpResponse
from datetime import datetime

from my_runs.models import Run, Split
from my_runs.garmin import GarminPortal


def index(request):
    return HttpResponse("Hello")


def run(request, run_id):
    print('hello')
    print(run_id)
    run = get_object_or_404(Run, activity_id=run_id)
    print(run)
    split_list = Split.objects.filter(run=run)
    return render(request, 'my_runs/run.html', {'run': run, 'split_list': split_list})


def create_run_entry():
    gp = GarminPortal()
    #run_data = gp.get_all_summary_activities()
    run_data = gp.get_new_summary_activties((0,3))
    split_data = gp.get_split_of_activities(run_data)
    for run in run_data:
        try:
            if run['activityType']['typeKey'] == 'lap_swimming':
                #todo fix for all exercise types
                continue
            name = run['activityName']
            date = run['startTimeLocal'].split(" ")[0]
            activity_id = run['activityId']
            duration = run['duration']
            distance = run['distance']

            r = Run(activity_id=activity_id, name=name, date=date, distance=distance, duration=duration)
            r.save()

            splits = split_data[activity_id]

            for key, split in splits.items():
                split_number = key
                elapsed_time = convert(split['elapsed_time'])
                moving_time = convert(split['moving_time'])
                avg_pace = convert(split['avg_pace'])
                s = Split(run=r, split_number=split_number, elapsed_time=elapsed_time, moving_time=moving_time,
                          avg_pace=avg_pace)
                s.save()
        except Exception as ex:
            print(ex)
            print(run)
            print(activity_id)
            print(splits)
            continue


def convert(time: str):
    time = time.strip()
    time_format = "%H:%M:%S.%f" if time.find(".") != -1 else "%H:%M:%S"
    return datetime.strptime(time, time_format)


def format_duration(run):
    import pytz
    from datetime import datetime, timedelta
    start_time = pytz.utc.localize(datetime.strptime(run["startTimeGMT"], "%Y-%m-%d %H:%M:%S"))
    end_time = start_time + timedelta(0, float(run["elapsedDuration"])/1000)
    diff = end_time - start_time
    seconds_in_day = 24 * 60 * 60
    mins, secs = divmod(diff.days * seconds_in_day + diff.seconds, 60)
    #fix this for hours
    return "00:{}:{}".format(mins, secs)