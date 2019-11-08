from django import forms


class NewSprintForm(forms.Form):
    effort_hours = forms.IntegerField(required=True, label='', widget=forms.NumberInput(attrs={
        "class": "form-control input-field",
        "style": "width: 200px;",
        "placeholder": "Effort Hours"
    }))
