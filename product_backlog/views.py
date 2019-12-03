import json
import uuid
from datetime import datetime, timedelta

from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
# Create your views here.
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from product_backlog.forms import CreatePBIV, CreatePBIVeri
from product_backlog.models import ProductBacklogItem
from product_log.models import Product
from sprint_backlog.models import Sprint
from utilities.constants.RoleEnum import STARTED, CREATED, TO_DO, IN_PROGRESS, COMPLETED, NOT_FINISHED

# helper function for getting the pbis of a product
def get_pbis(prod_id):
    pbis = ProductBacklogItem.objects.filter(product_id=prod_id).order_by('product_backlog_priority')
    pbis_current = ProductBacklogItem.objects.filter(product_id=prod_id,
                                                     product_status__in=[TO_DO, IN_PROGRESS]).order_by(
        'product_backlog_priority')
    product_name = Product.objects.filter(product_id=prod_id)[0].product_name
    product_id = Product.objects.filter(product_id=prod_id)[0].product_id
    return {
        'pbis': pbis,
        'pbis_current': pbis_current,
        'product_name': product_name,
        'product_id': product_id
    }


def check_sprint_status(current_sprint):
    print("1")
    enable_add_sprint = False
    if current_sprint is None:
        print("2")
        enable_add_sprint = True
    else:
        print("3")
        if model_to_dict(current_sprint)['end_time'] is None:
            print("4")
            return enable_add_sprint, current_sprint
        print(model_to_dict(current_sprint)['end_time'] < timezone.now())
        if model_to_dict(current_sprint)['end_time'] < timezone.now():
            print("abc")
            ProductBacklogItem.objects.filter(
                Q(product_backlog_sprint_id=current_sprint.sprint_id) & ~Q(product_status=COMPLETED)).update(
                product_status=NOT_FINISHED, product_backlog_sprint_id=None)
            current_sprint.status = COMPLETED
            current_sprint.save()
            enable_add_sprint = True
    return enable_add_sprint, current_sprint


def pbis_view(request, *args, **kwargs):
    if request.method == 'GET':
        result = get_pbis(kwargs['productid'])
        pbis = result['pbis']
        pbis_current = result['pbis_current']
        product_name = result['product_name']
        product_id = result['product_id']
    # if request.method == 'GET':
    product_instance = Product.objects.get(product_id=product_id)

    form = CreatePBIV(product_id=product_instance, product_backlog_id=uuid.uuid1())

    try:
        current_sprint = Sprint.objects.get(Q(status=CREATED) | Q(status=STARTED))
    except:
        current_sprint = None
    enable_add_sprint, current_sprint = check_sprint_status(current_sprint)
    return render(request, 'pbis.html', {'pbis': pbis,
                                         "show_add_to_sprint": not enable_add_sprint,
                                         'pbis_current': pbis_current,
                                         'title': 'PBIs of ' + product_name,
                                         'create_pbi': form,
                                         'product_id': kwargs['productid']
                                         })


def pbis_create(request, *args, **kwargs):
    if request.method == 'POST':
        form = CreatePBIVeri(request.POST)
        if form.is_valid():
            pbi = form.save(commit=False)
            pbi.save()
        return HttpResponseRedirect("/pbis/" + request.POST['product_id'])


def pbis_edit(request, *args, **kwargs):
    if request.method == 'POST':
        pbi_instance = ProductBacklogItem.objects.filter(product_backlog_id=request.POST['product_backlog_id']).first()
        form = CreatePBIVeri(request.POST, instance=pbi_instance)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/pbis/" + request.POST['product_id'])
    else:
        product_id = request.GET.get('product_id').split(" ")[2]
        product_id = product_id[1:len(product_id) - 1]
        pbi_instance = ProductBacklogItem.objects.filter(
            product_backlog_id=request.GET.get('product_backlog_id')).first()
        pbis = ProductBacklogItem.objects.filter(product_id=product_id).order_by('product_backlog_priority')
        pbis_current = ProductBacklogItem.objects.filter(product_id=product_id,
                                                         product_status=[TO_DO, IN_PROGRESS]).order_by(
            'product_backlog_priority')
        product_name = Product.objects.filter(product_id=product_id)[0].product_name
        form = CreatePBIVeri(instance=pbi_instance)
    return render(request, 'pbis_edit.html', {'pbis': pbis,
                                              'pbis_current': pbis_current,
                                              'title': 'PBIs of ' + product_name,
                                              'create_pbi': form,
                                              })


@csrf_exempt
def add_to_sprint_backlog(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    product_id = body['pbi']
    current_sprint = Sprint.objects.get(Q(status=CREATED) | Q(status=STARTED))
    if current_sprint.status == CREATED:
        current_sprint.status = STARTED
        current_sprint.start_time = datetime.now()
        current_sprint.end_time = current_sprint.start_time + timedelta(days=15)
        current_sprint.save()
    ProductBacklogItem.objects.filter(product_backlog_id=product_id).update(
        product_backlog_sprint_id=current_sprint.sprint_id, product_status=IN_PROGRESS)


@csrf_exempt
def delete_pbi(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    product_backlog_id = body['pbi']
    product_id = body['product_id']
    product_id = product_id.split(" ")[2]
    product_id = product_id[1:len(product_id) - 1]
    # getting the instance
    instance = ProductBacklogItem.objects.get(product_backlog_id=product_backlog_id)
    instance.delete()
    return JsonResponse({'foo': 'bar'})
