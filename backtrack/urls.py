"""backtrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from django.contrib import admin

from product_log.views import product_backlog_view
from sprint_backlog.views import get_sprint_backlog
from user_registration.views import login_view, sign_up_view
from product_backlog.views import pbis_view, pbis_create, pbis_edit, add_to_sprint_backlog,delete_pbi

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('login/', login_view),
    url('signUp/', sign_up_view),
    url('productBacklog/', product_backlog_view),
    path('pbis/<slug:productid>', pbis_view, name='pbis'),
    path('pbisedit/', pbis_edit, name='pbisedit'),
    url('addToSprintBacklog', add_to_sprint_backlog, name='addToSprintBacklog'),
    url('deletePbi', delete_pbi, name='deletePbi'),
    url('pbiscreate', pbis_create),
    url('sprintBacklog', get_sprint_backlog),

]

handler404 = 'user_registration.views.view_404'
