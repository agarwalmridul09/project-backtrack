from datetime import datetime

from django.shortcuts import render

# Create your views here.
from sprint_backlog.forms import NewSprintForm
from sprint_backlog.models import SpringBacklog


def get_sprint_backlog(request, *args, **kwargs):
    if request.method == 'POST':
        form = NewSprintForm(request.POST)
        if form.is_valid():
            sprint_item = SpringBacklog.create(form.cleaned_data['effort_hours'])
            sprint_item.save()
    else:
        form = NewSprintForm()
    current_sprint = SpringBacklog.objects.filter(end_time__gt=datetime.now()).first()
    return render(request, 'sprint_backlog.html', {"create_sprint": form})
