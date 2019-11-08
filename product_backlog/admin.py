from django.contrib import admin

# Register your models here.
from product_backlog.models import ProductBacklogItem

admin.site.register(ProductBacklogItem)
