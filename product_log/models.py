from django.db import models

# Create your models here.
from user_registration.models import User


class Product(models.Model):
    product_id = models.CharField(primary_key=True, max_length=16)
    product_name = models.CharField(null=False, max_length=50)
    product_manager = models.ForeignKey(User, to_field='email', on_delete=models.CASCADE,
                                        related_name='product_manager')
    product_owner = models.ForeignKey(User, to_field='email', on_delete=models.CASCADE, related_name='product_owner')
    start_date = models.DateField()
    end_date = models.DateField()


class Developers(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    developer_id = models.ForeignKey(User, to_field='email', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, to_field='product_id', on_delete=models.CASCADE)
