import uuid

from django.db import models

from utilities.constants.RoleEnum import SprintStatus, CREATED


class Sprint(models.Model):
    sprint_id = models.CharField(primary_key=True, max_length=200)
    effort_hours = models.PositiveIntegerField()
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=200, choices=SprintStatus, default=CREATED)
    objects = models.Manager()

    @classmethod
    def create(cls, effort_hours):
        sprint_id = uuid.uuid1()
        return cls(sprint_id=sprint_id, effort_hours=effort_hours)
