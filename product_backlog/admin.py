from django.contrib import admin

# Register your models here.
from product_backlog.models import ProductBacklogItem, PBITask

admin.site.register(ProductBacklogItem)
admin.site.register(PBITask)
