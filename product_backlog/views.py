from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import uuid

# Create your views here.
from product_backlog.forms import  CreatePBIV, CreatePBIVeri
from product_backlog.models import ProductBacklog
from product_log.models import Product

def pbis_view(request,  *args, **kwargs):
    if request.method == 'GET':
            pbis = ProductBacklog.objects.filter(product_id=kwargs['productid']).order_by('product_backlog_priority')
            product_name = Product.objects.filter(product_id=kwargs['productid'])[0].product_name
            product_id = Product.objects.filter(product_id=kwargs['productid'])[0].product_id

    product_instance=Product.objects.get(product_id=product_id)

    form = CreatePBIV(product_id=product_instance,product_backlog_id=uuid.uuid1())

    return render(request, 'pbis.html', {'pbis':pbis,
                                         'title':'PBIs of '+product_name,
                                         'create_pbi':form,
                                         'product_id':kwargs['productid']
                                            })

def pbis_create(request,  *args, **kwargs):
    if request.method == 'POST':
        form = CreatePBIVeri(request.POST)
        if form.is_valid():
            pbi = form.save(commit=False)
            pbi.save()
        return HttpResponseRedirect("/pbis/"+request.POST['product_id'])

def pbis_edit(request,  *args, **kwargs):
    if request.method == 'POST':
        pbi_instance = ProductBacklog.objects.filter(product_backlog_id=request.POST['product_backlog_id']).first()
        form = CreatePBIVeri(request.POST, instance=pbi_instance)
        if form.is_valid():      
            form.save()
        return HttpResponseRedirect("/pbis/"+request.POST['product_id'])
    else:
        product_id = request.GET.get('product_id').split(" ")[2]
        product_id = product_id[1:len(product_id)-1]
        pbi_instance = ProductBacklog.objects.filter(product_backlog_id=request.GET.get('product_backlog_id')).first()
        pbis = ProductBacklog.objects.filter(product_id=product_id).order_by('product_backlog_priority')
        product_name = Product.objects.filter(product_id=product_id)[0].product_name
        form = CreatePBIVeri(instance=pbi_instance)
    return render(request, 'pbis_edit.html', {'pbis':pbis,
                                         'title':'PBIs of '+product_name,
                                         'create_pbi':form,
                                            })
