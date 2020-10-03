from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
import pandas as pd

from .models import Run, Split


def run(request, run_id):
    run = get_object_or_404(Run, pk=run_id)
    split_list = Split.objects.filter(run=run)
    return render(request, 'my_runs/run.html', {'run': run, 'split_list': split_list})


def create_run_entry():
    p = '/Users/caitlinhamilton/Programming/RunningApp/MyRunningApp/my_running_app/my_runs/garmin/activity.csv'
    df = pd.read_csv(p)

    activity_id = 5
    name = df['activityName'].loc[0]
    date = df['startTimeLocal'].loc[0]
    distance = df['distance'].loc[0]
    # duration = df['duration'].loc[0]
    print(name)

    r = Run(activity_id=activity_id, name=name, date=date, distance=distance)
    r.save()

    s = Split(run=r, duration= '14:30:59', avg_pace='14:30:59')
    s.save()

    s = Split(run=r, duration='15:30:59', avg_pace='15:30:59')
    s.save()


def create_split_entry():
    p = '/Users/caitlinhamilton/Programming/RunningApp/MyRunningApp/my_running_app/my_runs/garmin/split.csv'
    df = pd.read_csv(p)
    # run = models.ForeignKey(Run, on_delete=models.CASCADE)
    # #one to many- One run has many splits
    # duration = models.TimeField()
    # avg_pace = models.TimeField()
    s = Split(run= r, duration= '14:30:59', avg_pace='14:30:59')
