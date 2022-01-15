from django.db import models


class Run(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    distance = models.FloatField(max_length=200)
    duration = models.FloatField(max_length=200)

    def __str__(self):
        return str(self.id)


class Split(models.Model):
    run = models.ForeignKey(Run, related_name='splits', on_delete=models.CASCADE)
    split_number = models.IntegerField()
    elapsed_time = models.FloatField(max_length=200)
    moving_time = models.FloatField(max_length=200)
    avg_pace = models.FloatField(max_length=200)

    def __str__(self):
        return str(self.split_number)

# fields
#'Split', 'Time', 'Moving Time', 'Distance', 'Elevation Gain', 'Elev Loss', 'Avg Pace',
# 'Avg Moving Paces', 'Best Pace', 'Avg Run Cadence', 'Max Run Cadence', 'Avg Stride Length',
# 'Avg HR', 'Max HR', 'Avg Temperature', 'Calories']


