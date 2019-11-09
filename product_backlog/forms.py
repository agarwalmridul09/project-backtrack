from django import forms
from django.forms import ModelForm

from product_backlog.models import ProductBacklogItem
from user_registration.models import User
from utilities.constants import RoleEnum
from utilities.constants.RoleEnum import SprintStatus


class CreatePBIV(ModelForm):
    class Meta:
        model = ProductBacklogItem
        fields= [
            'product_id',
            'product_backlog_title',
            'product_backlog_description',
            'product_status',
            'product_backlog_story_points',
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
            'product_backlog_story_points',
            'product_backlog_id',
            'product_backlog_priority'
        ]

        widgets = {'product_id': forms.HiddenInput(), "product_backlog_id": forms.HiddenInput()}


class CreateTask(forms.Form):
    title = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={
        "class": "form-control input-field",
        "placeholder": "Task Name"
    }))

    description = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={
        "class": "form-control input-field",
        "placeholder": "Task Description"
    }))
    effort_hours = forms.IntegerField(required=True, label='', widget=forms.NumberInput(attrs={
        "class": "form-control input-field",
        "placeholder": "Effort Hours"
    }))

    owner = forms.ModelChoiceField(queryset=User.objects.filter(role=RoleEnum.DEVELOPER),
                                   widget=forms.Select(attrs={
                                       "class": "form-control input-field",
                                   }))

    status = forms.ChoiceField(choices=SprintStatus,
                               widget=forms.Select(attrs={
                                   "class": "form-control input-field",
                               }))
    pbi_id_id = forms.CharField(widget=forms.HiddenInput(attrs={
        "id": "pbi-id",
        "class": "form-control input-field",
    }))

    # def __init__(self, *args, **kwargs):
    #     initial = kwargs.pop('initial', None)
    #     if initial:
    #         self.status = forms.ChoiceField(choices=SprintStatus,
    #                                         widget=forms.Select(attrs={
    #                                             "class": "form-control input-field",
    #                                         }))
    #         kwargs['initial'] = initial
    #     super(CreateTask, self).__init__(*args, **kwargs)
