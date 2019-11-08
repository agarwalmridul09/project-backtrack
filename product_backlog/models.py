from django.db import models

from product_log.models import Product
from sprint_backlog.models import Sprint
from user_registration.models import User
from utilities.constants.RoleEnum import PBIStatus, TO_DO, SprintStatus, CREATED


class ProductBacklogItem(models.Model):
    product_backlog_id = models.CharField(primary_key=True, max_length=200)
    product_backlog_title = models.CharField(max_length=200)
    product_backlog_description = models.TextField()
    product_id = models.ForeignKey(Product, to_field='product_id', on_delete=models.CASCADE, related_name="pbi_product_id")
    product_status = models.CharField(max_length=200, choices=PBIStatus, default=TO_DO)
    product_backlog_sprint = models.CharField(max_length=200)
    product_backlog_priority = models.CharField(max_length=200, default='1')
    product_backlog_sprint_id = models.ForeignKey(Sprint, to_field='sprint_id', on_delete=models.CASCADE,
                                                  related_name='product_backlog_sprint_id', null=True, blank=True)

    objects = models.Manager()


class PBITask(models.Model):
    task_id = models.CharField(primary_key=True, max_length=200)
    pbi_id = models.ForeignKey(ProductBacklogItem, to_field='product_backlog_id', on_delete=models.CASCADE,
                               related_name='task_id')
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=200, choices=SprintStatus, default=CREATED)
    description = models.TextField()
    owner = models.ForeignKey(User, to_field='email', on_delete=models.CASCADE,
                              related_name='task_owner')
    effort_hours = models.PositiveIntegerField()
    objects = models.Manager()

