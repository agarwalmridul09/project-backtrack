from django.db import models

from product_log.models import Product
from sprint_backlog.models import SpringBacklog
from utilities.constants.RoleEnum import PBIStatus, TO_DO


class ProductBacklog(models.Model):
    product_backlog_id = models.CharField(primary_key=True, max_length=200)
    product_backlog_title = models.CharField(max_length=200)
    product_backlog_description = models.CharField(max_length=200)
    product_id = models.ForeignKey(Product, to_field='product_id', on_delete=models.CASCADE, related_name="pbi_product_id")
    product_status = models.CharField(max_length=200, choices=PBIStatus, default=TO_DO)
    product_backlog_sprint = models.CharField(max_length=200)
    product_backlog_priority = models.CharField(max_length=200, default='1')
    product_backlog_sprint_id = models.ForeignKey(SpringBacklog, to_field='sprint_id', on_delete=models.CASCADE,
                                                  related_name='product_backlog_sprint_id', null=True, blank=True)
