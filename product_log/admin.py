from django.contrib import admin

# Register your models here.
from product_log.models import Product, Developers

admin.site.register(Product)
admin.site.register(Developers)
