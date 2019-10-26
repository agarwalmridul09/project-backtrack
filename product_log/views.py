import uuid

from django.shortcuts import render

# Create your views here.
from product_log.forms import CreateProduct
from product_log.models import Product


def product_backlog_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = CreateProduct(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            product = Product.objects.create(product_id=uuid.uuid1(), product_name=cleaned_data['product_name'],
                                             product_owner=cleaned_data['product_owner'],
                                             product_manager=cleaned_data['product_manager'],
                                             start_date=cleaned_data['start_date'],
                                             end_date=cleaned_data['end_date'])
            print(product)
            product.save()
    else:
        form = CreateProduct()
    products = Product.objects.all()
    return render(request, 'backlog.html', {'products': products,
                                            'title': "All Products",
                                            "create_product": form})

