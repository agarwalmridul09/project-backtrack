import json
import uuid

from django.db.models import Q, Sum
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.defaultfilters import register
from django.views.decorators.csrf import csrf_exempt

from product_backlog.forms import CreateTask
from product_backlog.models import ProductBacklogItem, PBITask
from sprint_backlog.forms import NewSprintForm
from sprint_backlog.models import Sprint
from user_registration.models import User
from utilities.constants.RoleEnum import CREATED, STARTED, COMPLETED, SprintStatus, PBIStatus


def get_sprint_backlog(request, *args, **kwargs):
    if request.method == 'POST':
        form = NewSprintForm(request.POST)
        if form.is_valid():
            sprint_item = Sprint.create(form.cleaned_data['effort_hours'])
            sprint_item.save()
    else:
        form = NewSprintForm()
    product_backlogs = None
    effort_hours_by_pbis_dict = None
    percent_done = 0
    effort_hours_by_pbis_of_tasks_done_dict = None
    percent_done_by_pbis_dict = {}
    try:
        current_sprint = Sprint.objects.get(Q(status=CREATED) | Q(status=STARTED))
        product_backlogs = ProductBacklogItem.objects.filter(product_backlog_sprint_id=current_sprint.sprint_id)
        effort_hours_by_pbis = PBITask.objects.all().values('pbi_id').annotate(sumsize=Sum('effort_hours'))
        effort_hours_by_pbis_of_tasks_done = PBITask.objects.filter(Q(status=COMPLETED)).values('pbi_id').annotate(sumsize=Sum('effort_hours'))
        hours_done = PBITask.objects.filter(Q(status=COMPLETED)).aggregate(Sum('effort_hours'))
        total_hours = PBITask.objects.aggregate(Sum('effort_hours'))
        percent_done = (hours_done['effort_hours__sum'] / total_hours['effort_hours__sum'])*100
        effort_hours_by_pbis_dict = {}
        for entry in effort_hours_by_pbis:
            effort_hours_by_pbis_dict[entry['pbi_id']] = entry['sumsize']
        effort_hours_by_pbis_of_tasks_done_dict = {}
        for entry in effort_hours_by_pbis_of_tasks_done:
            effort_hours_by_pbis_of_tasks_done_dict[entry['pbi_id']] = entry['sumsize']
        for key, val in effort_hours_by_pbis_dict.items():
            done_hours = 0
            if key in effort_hours_by_pbis_of_tasks_done_dict:
                done_hours = effort_hours_by_pbis_of_tasks_done_dict[key]
            percent_done_by_pbis_dict[key] = round((done_hours / val) * 100 , 2)
    except:
        current_sprint = None
    add_task_form = CreateTask()
    enable_add_sprint = False
    if current_sprint is None:
        enable_add_sprint = True
    return render(request, 'sprint_backlog.html',
                  {"title": "Sprint Backlog", "create_sprint": form, "enable_add_sprint": enable_add_sprint,
                   "product_backlogs": product_backlogs,
                   "percent_done_by_pbis_dict": percent_done_by_pbis_dict,
                   "sprint_status_enum": SprintStatus,
                   "pbi_status_enum": PBIStatus,
                   "add_task_form": add_task_form,
                   "percent_sprint_done": round(percent_done, 2),
                   "effort_hours_by_pbis_of_tasks_done_dict": effort_hours_by_pbis_of_tasks_done_dict,
                   "effort_hours_by_pbis": effort_hours_by_pbis_dict
                   })


def add_task(request, *args, **kwargs):
    if request.method == 'POST':
        form = CreateTask(request.POST)
        if form.is_valid():
            task = PBITask.objects.create(**form.cleaned_data, task_id=uuid.uuid1())
            task.save()
    return HttpResponseRedirect("/sprintBacklog")


@csrf_exempt
def edit_task(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    task_id = body['taskID']
    task_instance = PBITask.objects.get(Q(task_id=task_id))
    task_instance = model_to_dict(task_instance)
    user = User.objects.get(Q(email=task_instance['owner']))
    pbi = ProductBacklogItem.objects.get(Q(product_backlog_id=task_instance['pbi_id']))
    task_instance['owner'] = user
    task_instance['pbi_id_id'] = model_to_dict(pbi)['product_backlog_id']
    form = CreateTask(initial=task_instance)
    return render(request, 'edit_task.html',
                  {"edit_task_form": form,
                   "task_id": task_instance['task_id']
                   })


@csrf_exempt
def remove_pbi_from_sprint(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    pbi_id = body['PBIId']
    ProductBacklogItem.objects.filter(Q(product_backlog_id=pbi_id)).update(product_backlog_sprint_id=None)
    return HttpResponseRedirect("/sprintBacklog")


@csrf_exempt
def remove_task(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    task_id = body['taskID']
    PBITask.objects.filter(Q(task_id=task_id)).delete()
    return HttpResponseRedirect("/sprintBacklog")


def update_task(request, task_id):
    form = CreateTask(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        data['owner'] = data['owner'].email
        data['pbi_id_id'] = data['pbi_id_id']
        PBITask.objects.filter(Q(task_id=task_id)).update(**form.cleaned_data)
    return HttpResponseRedirect("/sprintBacklog")


@register.filter
def get_item(dictionary, key):
    try:
        return dictionary[key]
    except:
        return 0


@register.filter
def get_enum_val(a, key):
    for  i in a:
        if i[0] == key:
            return i[1]
    return key
