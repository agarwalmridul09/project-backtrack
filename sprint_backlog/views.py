from datetime import datetime
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from sprint_backlog.forms import NewSprintForm
from sprint_backlog.models import SprintBacklog
from utilities.constants.RoleEnum import CREATED, STARTED


def get_sprint_backlog(request, *args, **kwargs):
    if request.method == 'POST':
        form = NewSprintForm(request.POST)
        if form.is_valid():
            sprint_item = SprintBacklog.create(form.cleaned_data['effort_hours'])
            sprint_item.save()
    else:
        form = NewSprintForm()
    current_sprint = SprintBacklog.objects.filter(Q(status=CREATED) | Q(status=STARTED)).first()
    enable_add_sprint = False
    if current_sprint is None:
        enable_add_sprint = True
    return render(request, 'sprint_backlog.html', {"create_sprint": form, "enable_add_sprint": enable_add_sprint})
