from django.contrib import admin

# Register your models here.
from product_log.models import Product, Developer

admin.site.register(Product)
admin.site.register(Developer)
