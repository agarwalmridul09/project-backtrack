from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from product_backlog.models import ProductBacklogItem
from sprint_backlog.forms import NewSprintForm
from sprint_backlog.models import Sprint
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
    except:
        current_sprint = None
    # product_backlogs = ProductBacklogItem.objects.filter(product_backlog_sprint_id=current_sprint.sprint_id)
    enable_add_sprint = False
    if current_sprint is None:
        enable_add_sprint = True
    return render(request, 'sprint_backlog.html',
                  {"title": "Sprint Backlog", "create_sprint": form, "enable_add_sprint": enable_add_sprint,
                   })
