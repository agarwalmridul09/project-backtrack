from django import forms
from django.forms import ModelForm

from product_backlog.models import ProductBacklogItem
from product_log.models import Product
from utilities.constants import RoleEnum
from user_registration.models import User
import uuid



class CreatePBIV(ModelForm):
    class Meta:
        model = ProductBacklogItem
        fields= [
            'product_id',
            'product_backlog_title',
            'product_backlog_description',
            'product_status',
            'product_backlog_sprint',
            'product_backlog_id',
            'product_backlog_priority'
        ]
        widgets = {'product_id': forms.HiddenInput(), "product_backlog_id": forms.HiddenInput(), "product_status": forms.HiddenInput()}

    def __init__(self, product_id, product_backlog_id,  *args, **kwargs):
        super(CreatePBIV, self).__init__(*args, **kwargs)
        self.fields['product_id'].initial = product_id
        self.fields['product_backlog_id'].initial = product_backlog_id
        self.fields['product_status'].initial = RoleEnum.TO_DO

class CreatePBIVeri(ModelForm):
    class Meta:
        model = ProductBacklogItem
        fields= [
            'product_id',
            'product_backlog_title',
            'product_backlog_description',
            'product_status',
            'product_backlog_sprint',
            'product_backlog_id',
            'product_backlog_priority'
        ]

        widgets = {'product_id': forms.HiddenInput(), "product_backlog_id": forms.HiddenInput()}





