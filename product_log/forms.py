from django import forms

from user_registration.models import User
from utilities.constants import RoleEnum


class CreateProduct(forms.Form):
    product_name = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={
        "class": "form-control input-field",
        "placeholder": "Product Name"
    }))

    product_owner = forms.ModelChoiceField(queryset=User.objects.filter(role=RoleEnum.PRODUCT_OWNER),
                                           widget=forms.Select(attrs={
                                               "class": "form-control input-field",
                                           }))
    product_manager = forms.ModelChoiceField(queryset=User.objects.filter(role=RoleEnum.MANAGER),
                                             widget=forms.Select(attrs={
                                                 "class": "form-control input-field",
                                             }))
    developers = forms.ModelChoiceField(queryset=User.objects.filter(role=RoleEnum.DEVELOPER),
                                        widget=forms.SelectMultiple(attrs={
                                            "class": "form-control input-field",
                                        }))
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(attrs={
            "class": "form-control input-field",
            "style": "display: inline-block; width: auto; vertical-align: middle;"
        }))
    end_date = forms.DateField(
        widget=forms.SelectDateWidget(attrs={
            "class": "form-control input-field",
            "style": "display: inline-block; width: auto; vertical-align: middle;"
        }))
    # developer = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
    #                                       choices=User.objects.filter(role=RoleEnum.DEVELOPER).all().values_list(
    #                                           'email', 'first_name'))
