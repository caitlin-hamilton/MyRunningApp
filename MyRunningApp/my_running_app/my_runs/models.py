from django.db import models


class Run(models.Model):
    activity_id = models.IntegerField()
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    #'2020-09-30 16:14:23' StartTimeLocal
    distance = models.CharField(max_length=200)
    #change above to float
    # duration = models.TimeField()
    # investigate timefields
    #'elapsedDuration', 'movingDuration', 'elevationGain', 'elevationLoss', 'averageSpeed', 'maxSpeed'

    def __str__(self):
        return self.name


class Split(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    #one to many- One run has many splits
    duration = models.TimeField()
    avg_pace = models.TimeField()


#'Split', 'Time', 'Moving Time', 'Distance', 'Elevation Gain', 'Elev Loss', 'Avg Pace', 'Avg Moving Paces', 'Best Pace', 'Avg Run Cadence', 'Max Run Cadence', 'Avg Stride Length', 'Avg HR', 'Max HR', 'Avg Temperature', 'Calories']


