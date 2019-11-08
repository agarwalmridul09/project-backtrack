import uuid
from datetime import datetime, timedelta

from django.db import models


class SpringBacklog(models.Model):
    sprint_id = models.CharField(primary_key=True, max_length=200)
    effort_hours = models.IntegerField()
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    objects = models.Manager()

    @classmethod
    def create(cls, effort_hours):
        sprint_id = uuid.uuid1()
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=effort_hours)
        return cls(sprint_id=sprint_id, effort_hours=effort_hours, start_time=start_time, end_time=end_time)
