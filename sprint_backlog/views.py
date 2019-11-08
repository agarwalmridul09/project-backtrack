import json
import uuid

from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from product_backlog.forms import CreateTask
from product_backlog.models import ProductBacklogItem, PBITask
from sprint_backlog.forms import NewSprintForm
from sprint_backlog.models import Sprint
from user_registration.models import User
from utilities.constants.RoleEnum import CREATED, STARTED


def get_sprint_backlog(request, *args, **kwargs):
    if request.method == 'POST':
        form = NewSprintForm(request.POST)
        if form.is_valid():
            sprint_item = Sprint.create(form.cleaned_data['effort_hours'])
            sprint_item.save()
    else:
        form = NewSprintForm()
    try:
        current_sprint = Sprint.objects.get(Q(status=CREATED) | Q(status=STARTED))
        product_backlogs = ProductBacklogItem.objects.filter(product_backlog_sprint_id=current_sprint.sprint_id)
    except:
        current_sprint = None
        product_backlogs = None
    add_task_form = CreateTask()
    enable_add_sprint = False
    if current_sprint is None:
        enable_add_sprint = True
    return render(request, 'sprint_backlog.html',
                  {"title": "Sprint Backlog", "create_sprint": form, "enable_add_sprint": enable_add_sprint,
                   "product_backlogs": product_backlogs,
                   "add_task_form": add_task_form
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


def update_task(request, task_id):
    form = CreateTask(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        data['owner'] = data['owner'].email
        data['pbi_id_id'] = data['pbi_id_id']
        PBITask.objects.filter(Q(task_id=task_id)).update(**form.cleaned_data)
    return HttpResponseRedirect("/sprintBacklog")
