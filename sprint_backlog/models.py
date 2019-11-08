import uuid
from datetime import datetime, timedelta

from django.db import models

from utilities.constants.RoleEnum import SprintStatus, CREATED, COMPLETED, STARTED


class SprintBacklog(models.Model):
    sprint_id = models.CharField(primary_key=True, max_length=200)
    effort_hours = models.IntegerField()
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=200, choices=SprintStatus, default=CREATED)
    objects = models.Manager()

    @classmethod
    def create(cls, effort_hours):
        sprint_id = uuid.uuid1()
        # start_time = datetime.now()
        # end_time = start_time + timedelta(days=15)
        return cls(sprint_id=sprint_id, effort_hours=effort_hours)

    # @property
    # def status(self):
    #     if self.end_time > datetime.now():
    #         return COMPLETED
    #     if self.start_time is None:
    #         return CREATED
    #     return STARTED
